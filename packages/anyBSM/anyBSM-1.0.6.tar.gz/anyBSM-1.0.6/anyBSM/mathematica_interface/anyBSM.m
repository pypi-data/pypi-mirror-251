Code[str_]:=Style[str,Gray];
Print[Style["anyBSM ","Section",FontSize->22],Style["Mathematica interface" ,"Section",FontSize->15]];
Print[Style["Copyright by Henning Bahl, Johannes Braathen, Martin Gabelmann, Georg Weiglein.", Gray, FontSize-> 10]];
Print[Style["If you need any help, please contact the ", Black],Hyperlink["online documentation","https://anybsm.gitlab.io/anybsm/anyBSM.html"]];

Eval::usage = "Wrapper around ExternalEvaluate[$Session, \"command-to-excute\"]";
$AnyFunctions::usage = "List constaining all Mathematica functions and their python-equivalent. Python functions starting with \"model.\" are wrappers around anyBSM.anyBSM.<function>";
LoadModel::usage = "LoadModel[\"model name or path to a UFO model\"] initializes the anyBSM model and stores it in the variable \"model\" withing the python session $Session.
Wrapper around \"anyBSM.anyBSM/anyModel\". See also Options[LoadModel].";
getOptions::usage = "Takes a python function/class and returns its optional arguments (kwargs)";
getArguments::usage = "Takes a python function/class and returns its positional arguments";
Py2Math::usage = "Creates a Mathematica-wrapper for a given ptyhon-function";
UVparts::usage = "replacement list which replaces common one-loop functions by ther UV-divergent parts";
getcoupling::usage = "getcoupling[\"f1\", \"f2\", ...] searches for the couplings of the fields f1,f2,... in the UFO file. Wrapper around anyBSM.anyModel.getcoupling";
setparameters::usage = "setparameters[parameter1 -> value1, ...] returns replacement list with relatations between internal/external parameters as well as numerical (default) values defined in the UFO model. Values can be overwritten. Example: setparameters[Mu3->175,Mh->126].";
parameters::usage = "Association of all UFO parameters and their properties";
internalparameters::usage = "analytical relations between input (external) and lagrangian (internal) parameters";
ListRenormalizationSchemes::usage = "`ListRenormalizationSchemes[]` lists renormalization schemes defined in the schemes.yml of the loaded model";
LoadRenormalizationScheme::usage = "`LoadRenormalizationScheme` loads a renormalization scheme defined in the schemes.yml of the loaded model. To get a list of all available schemes you can call `ListRenormalizationSchemes[]`";
AutoSolveDependencies::usage = "Resolving parameter dependencies is done in python by default. This can sometimes be more time consuming. Turn it off/on using `AutoSolveDependencies[False/True]` and instead use the replacement list `internalparameters`.";

If[$Session["Active"] == True,
    Print["Error: there is already an open Python session. Killing it..."];
    DeleteObject[$Session];
];


$AnyFunctions = {
{"$Session", "Variable containing the ExternalEvaluateObject of the python session"},
{Eval, "General wrapper around ExternalEvaluate[$Session]"},
{LoadModel, "anyBSM.anyModel"},
{"UVparts", UVparts::usage},
{"AutoSolveDependencies", AutoSolveDependencies::usage}
};

$Session = StartExternalSession["Python"];
Eval[expr_String]:=ExternalEvaluate[$Session,expr];
Print["Started a python "<>$Session["Version"] <> " kernel"];

import = ExternalEvaluate[$Session, "
try:
    from anyBSM import anyBSM, anyModel
    from sympy import mathematica_code
    from collections import defaultdict
    import inspect
    print('imported anyBSM and sympy')
    ret = True
except Exception as e:
    ret = str(e)
ret
"];

If[import=!=True, 
Print[Style["ERROR! ", Red], "could not import anyBSM. Error message was:"];
Print["    ", Style[import, Red]];
Print["Did you correctly install anyBSM with ", Code["python3 -m pip install --user anyBSM"], " ?"];
Abort[]
];

Print[Style["Tips for beginners:","Section", FontSize -> 18]];
Print["  * load a model with ", Code["LoadModel[\"modelname\"]"], " (e.g. ", Code["LoadModel[\"SM\"]"],")
  * list all available/built-in models with ", Code["ListModels[]"],"
  * ", Code["LoadModel"], " also takes absolute paths to any UFO model.
  * After loading a model:
    * calculate the trilinear Higgs coupling in a given model with ", Code["lambdahhh[]"], "
    * available function-wrappers are listed in ", Code["$AnyFunctions"], "
    * use Mathematicas help (e.g. ", Code["?getcoupling"], ") for any of the ", Code["$AnyFunction"], "s
    * the Mathematica-equivalent of ", Code["pyfunction(some='value')"], " is ", Code["mathfunction[\"some\"->\"'value'\"]"],"
      e.g. the python code ", Code["model.lambdahhh(momenta=['Mh1**2','Mh1**2','p2'])"], "
      in mathematica ", Code["lambdahhh[\"momenta\"->\"['Mh1**2','Mh1**2','p2']\"]"], "
      (i.e. all arguments are passed to the python compiler)
    * the loaded anyBSM model is stored within the current python session in the ", Code["model"], "-object.
      Any python command can be executed with the use of", Code["Eval"], ".
      For instance: 
        ", Code["Eval[\"model.set_evaluation_mode('numerical')\"]"], "
      changes the evaluation mode from 'analytical' (default) to 'numerical'.
"];

getOptions[func_String] := ToExpression[Eval["
params = inspect.signature(" <> func <> ").parameters
opts = []
for k,v in params.items():         
    if v.default != inspect._empty:
        if type(v.default) == str:
            t = \"\\'\"
        else:
            t = ''
        opts.append('\"' + k + '\" -> \"' + t + \
str(v.default) + t + '\"')

'{' + ','.join(opts) + '}'                                         
"]]

getArguments[func_String] := ToExpression[Eval["
params = inspect.signature(" <> func <> ").parameters
args = []
for k,v in params.items():
    if v.default == inspect._empty:
        if str(v).startswith('*'):
            args.append(v.name + '__')
        else:
            args.append(v.name + '_')
'{' + ','.join(args) + '}'                         
"]]

ArgList[fields__]:=Return["'" <> StringRiffle[List[fields],"','"] <> "'"]

ListModels[]:=Block[{models},
   models = Eval["anyBSM.built_in_models"];
   Print[
       Dataset[KeyValueMap[<|"Model name" -> #, "Path" -> #2|> &,  models]
       ,DatasetTheme -> "Detailed"][SortBy["Model name"]]
    ];
   Print["Tip: LoadModel[\"<model>\"] takes both, model names from above as well as arbitrary paths to any UFO model."];
   Return[Keys[models]];
];

Options[LoadModel] = getOptions["anyModel"];
SetOptions[LoadModel,{"caching" -> "2", "progress" -> "False", "quiet" -> "True", "evaluation" -> "'analytical'", "ask" -> "False"}];

LoadModel[Model_String,OptionsPattern[LoadModel]]:= Block[{opts},
    opts = Keys[Options[LoadModel]];
    ExternalEvaluate[$Session, "model = anyBSM(
    anyBSM.built_in_models.get('"<> Model <> "', '"<> Model <>"'),
    " <> StringRiffle[(# <> "=" <> OptionValue[#]) &/@ opts, ", "] <>"
    )
solvedependencies = True
def Math(expr, deps = False):
    global solvedependencies
    sympify = model.sympify
    if solvedependencies or deps:
        sympify = model.SolveDependencies
    try:
        if type(expr) == str:
            return mathematica_code(sympify(expr))
        elif type(expr) in [dict, defaultdict]:
            return {k : mathematica_code(sympify(v)) for k,v in expr.items()}
        return mathematica_code(expr)
    except:
        try:
            return str(expr)
        except:
            return expr
"];

(*link commonly used python functions*)
Py2Math["model.process", Process];
Py2Math["model.Tadpole", Tadpole, kwargsfrom -> "model.process"];
Py2Math["model.Sigma", Sigma, kwargsfrom -> "model.process", ignorekwargs -> {"momenta"}, addkwargs -> True];
Sigma[f1_, f2_, opts___] := Sigma[f1, "f2" -> "'" <> f2 <> "'", opts];
Sigmaprime[f1_,opts___]:=Sigma[f1,"derivative"->"True",opts];
Sigmaprime[f1_,f2_,opts___]:=Sigma[f1,f2,"derivative"->"True", opts];
Py2Math["model.lambdahhh", lambdahhh];
Py2Math["model.lambdahhhCT", lambdahhhCT];

If[$Assumptions===True,$Assumptions={g1>0,g2>0,g3>0,MWp>0,MWm>0,MZ>0,aEWM1>0}];
setparameters[];

Print[Style["Started model \""<> Model <> "\"", "Section", FontSize -> 12]];
Print["See ", Code["?$AnyFunctions"], " for available wrapper functions or directly calculate e.g. the trilinear Higgs selfcoupling using ",Code["lambdahhh[]"]];
];

AutoSolveDependencies[False]:=(Print["Will not resolve parameter dependencies within Python (you can use 'internalparameters' to do it in MMA)"];Eval["solvedependencies=False"])
AutoSolveDependencies[True]:=(Print["Will resolve parameter dependencies within Python"];Eval["solvedependencies=True"])

setPythonSignature[args_, opts_] := Block[{argsS = "", optsS = ""},
   If[args =!= {},
    argsS = ToString[#] &/@ args;
    argsS = DeleteCases[argsS, "kwargs__"|"args__"];
    argsS = ("\" <> ArgList["<>#<>"] <> \"")&/@ argsS;
    argsS = StringReplace[StringRiffle[argsS, ","], {"__"->"", "_"->""}];
    ];
   If[opts =!= {},
    optsS = (#[[1]] <> "= \" <> OptionValue[\"" <> #[[1]] <> "\"] <> \"") & /@ opts;
    optsS = StringRiffle[optsS, ", "];
    If[args =!= {}, optsS = ", " <> optsS];
    ];
   Return[argsS <> optsS]
];

Options[Py2Math] = {kwargsfrom->Null, ignorekwargs->{}, addkwargs -> False}
Py2Math[pyfunc_String, mathfunc_, OptionsPattern[Py2Math]] := Block[{args, argsS, opts, optspattern},
   args = getArguments[pyfunc];
   argsS = ToString[#] &/@ args;
   argsS = DeleteCases[argsS, "kwargs__"|"args__"];
   argsS = StringRiffle[argsS, ", "];
   opts = getOptions[pyfunc];
   If[Not[OptionValue[kwargsfrom] === Null], 
    If[OptionValue[addkwargs]==True,
      opts = Join[opts, getOptions[OptionValue[kwargsfrom]]],
      opts = getOptions[OptionValue[kwargsfrom]];
    ];
   ];
   opts = Select[opts, !MemberQ[OptionValue[ignorekwargs], #[[1]]]&];


   optspattern = "OptionsPattern[" <> ToString[mathfunc] <> "]";
   If[argsS =!= "", optspattern = " ," <> optspattern];
   exec = ToString[mathfunc] <> "[" <> argsS <> optspattern <> "] := Return[ToExpression[Eval[ \"Math(" <> pyfunc <> "(" <> setPythonSignature[args, opts] <> "))\"]]]";

   (*Print[FullForm[exec]];*)
   ClearAll[mathfunc];
   Options[mathfunc] = opts;
   mathfunc::usage = ExternalEvaluate[$Session, pyfunc <> ".__doc__"];
   ToExpression[exec];
   AppendTo[$AnyFunctions, {mathfunc,pyfunc}];
   Return[exec];
];



getcoupling[fields__]:=ToExpression[ExternalEvaluate[$Session,"
tmp = model.getcoupling(" <> ArgList[fields] <> ")
if not tmp:
    tmp = {}
for k,v in tmp.items():
    if hasattr(v, 'value'):
        tmp[k] = Math(tmp[k].value)
tmp"]];
AppendTo[$AnyFunctions, {getcoupling, "model.getcoupling"}];

setparameters[para___] := Block[{sym, paras, paralist = List[para]},
  Eval["model.parameters['SignSinThetaW'].value = 'SignSinThetaW'"];
  parameters = Eval["{k: p.__dict__ for k,p in model.parameters.items()}"];
  parameters = AssociationMap[
    (sym = ToExpression[#[[1]]];
      sym -> AssociationMap[(
          ToExpression[##[[1]]] -> Switch[##[[1]],
            "type", 
            If[##[[2]] === "real" && ! 
               MemberQ[$Assumptions, sym], $Assumptions = 
              Join[$Assumptions, {sym \[Element] Reals}]]; ##[[2]],
            "texname", ##[[2]],
            "value", 
            If[! FreeQ[paralist, sym], sym /. paralist, 
             If[Head[##[[2]]] === String, 
              ToExpression[
               Eval["mathematica_code(model.sympify('" <> 
                 ToString[##[[2]]] <> "'))"]], ##[[2]]]],
            __, ToExpression[#[[2]]]]
          ) &, #[[2]]]) &
    , parameters];
  Normal[ AssociationMap[#[[1]] -> #[[2]][value] &, parameters]]
]
AppendTo[$AnyFunctions, {setparameters, "model.setparameters"}];
AppendTo[$AnyFunctions, {HoldForm[parameters], "association with all UFO parameters"}];
internalparameters := (ToExpression[#[[1]]] ->  ToExpression[#[[2]]] & /@ Normal[Eval["{p.name: Math(p.name, True) for p in model.internal_parameters}"]])
AppendTo[$AnyFunctions, {HoldForm[internalparameters], "model.internal_parameters"}];

ListRenormalizationSchemes:=Datset[];
ListRenormalizationSchemes[]:=Block[{schemes},
   schemes = Eval["model.list_renormalization_schemes()"];
   Print[
       Dataset[KeyValueMap[<|"scheme name" -> #, "scheme info" -> #2|> &,  schemes]
       ,DatasetTheme -> "Detailed"][SortBy["scheme name"]]
    ];
   Return[Keys[schemes]];
];



AppendTo[$AnyFunctions, {HoldForm[ListRenormalizationSchemes], "model.list_renormalization_schemes"}];

LoadRenormalizationScheme[scheme_]:=Eval["model.load_renormalization_scheme('"<>ToString[scheme]<>"')"];
AppendTo[$AnyFunctions, {LoadRenormalizationScheme, "model.load_renormalization_scheme"}];


UVparts = {
   C0[__] :> 0,
   C1[__] :> 0,
   C2[__] :> 0,
   B0[__] :> 1/\[Epsilon],
   A0[x_] :> x/\[Epsilon],
   dB0[__] :> 0,
   B00[s_, x_, y_] :> 1/12 (3 x + 3 y - s)/\[Epsilon],
   dB00[__] :> -1/(12 \[Epsilon]),
   Dalpha -> 0
};
