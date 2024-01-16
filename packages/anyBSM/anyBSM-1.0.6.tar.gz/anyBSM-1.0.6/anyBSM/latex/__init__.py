__doc__ = r"""# $\LaTeX$ modules
This module consists of two sub-modules:
  * anyBSM.latex.printer  
    Utilities to convert UFO parameters into valid $\LaTeX$ (in case they
    have not a meaningful `texname` attribute). Also provides a
    sympy.printing.latex.LatexPrinter-class which is used to output
    symbols in their $\LaTeX$ representation when working in interactive
    Jupyter notebooks.
  * anyBSM.latex.drawer  
    A module which draws Feynman diagrams for a given set of
    internal/external fields as well as their results.

## How do I generate the Feynman diagrams?
### With the command line
```bash
anyH3 SM -e numerical -cc -R OS --tex 0.1
```
draws all Feynman diagrams involved in the calculation of the
trilinear Higgs self coupling - including those that enter the
counterterms. On the example above, only diagrams which contribute
with more than $0.1\text{GeV}^{n}$ are drawn. The option `--tex`
without any cut-off draws all diagrams.
For each amplitude a $\LaTeX$ file is generated at
```
<Path to UFO model>/latex/<model name>_<external states>_<evaluation
mode>_results.tex
```
I.e. the above command for the SM model generates the following files:
```console
$ ls -gG SM/latex/*pdf
-rw-r--r-- 1 121936 Jul 11 15:19 SM/latex/SM_hhh_numerical_results.pdf
-rw-r--r-- 1  75855 Jul 11 15:20 SM/latex/SM_AA_numerical_results.pdf
-rw-r--r-- 1 108158 Jul 11 15:20 SM/latex/SM_AZ_numerical_results.pdf
-rw-r--r-- 1 118399 Jul 11 15:19 SM/latex/SM_hh_numerical_results.pdf
-rw-r--r-- 1 147790 Jul 11 15:19 SM/latex/SM_WpWpc_numerical_results.pdf
-rw-r--r-- 1 138098 Jul 11 15:20 SM/latex/SM_ZZ_numerical_results.pdf
```
which are the diagrams for the triple-Higgs vertex and all
selfenergies entering the on-shell counterterms.
The `.tex` files are automatically compiled using
[lualatex](https://www.luatex.org/) which is available in the
package repositories of all common operation systems. The Diagrams are
generated with the help of $\TikzFeynman$ which is shipped with the
code (no separate installation required).

$\LaTeX$ output is also supported in the analytical/abbreviation
modes:
```bash
anyH3 SM -e analytical -cc -R OS --tex
```
which places the analytic results next to the Feynman diagrams. The
file names are as in the numerical case except that they do end with `*analytical_results.pdf`.

### With the library
The `anyBSM.anyProcess.anyProcess.process` function (as well as many
user functions such as anyBSM.anyH3.anyH3.lambdahhh) has a argument
`draw=True` which enables the $\LaTeX$ generation and compilation.
```python
from anyBSM import anyBSM
SM = anyBSM('SM', evaluation = 'numerical')
SM.Sigma('Wp',draw=True)
# returns W-selfenergy and writes diagrams to ~/SM_WpWpc_numerical_results.pdf as well as the model directory
```
The `draw` argument can again be a `bool` or a `float` but also an instance of anyBSM.latex.drawer.DrawProcess 
In the latter case, diagrams are added to the list of diagrams. anyBSM.latex.drawer.DrawProcess.write needs to 
be invoked yourself (see anyBSM.latex.drawer for more information).

## Compilation failed
Most likely there is a syntax error in one of the `texname`-fields of your
UFO model. Have a look at the `.log` files in the models `latex`
directory and try to compile the `.tex` files manually with different
compilers/flags. Also make sure that
[lualatex](https://www.luatex.org/) is installed and can be found 
on your system (e.g. issue `which lualatex`).

## How do I make use of $\LaTeX$ symbols in Jupyter?
The function `anyBSM.anyModel.anyModel.sympify_parameters` initializes
all UFO parameters as sympy parameters and also generates $\LaTeX$
representation for them as well as starts a printing session. It is
automatically called in the analytic evaluation mode:
```python
from anyBSM import anyBSM
SM = anyBSM('SM', evaluation = 'analytical')
hhhcoupling = SM.sympify(SM.getcoupling('h','u3','u3bar')['L'].value)
hhhcoupling # this should render '- \\frac{\\sqrt{2} i Yu_{33}}{2}' 

from sympy import latex
latex(hhhcoupling) # returns latex string
```

If everything fails, you can create your own sympy printer like this:
```python
from anyBSM.latex.printer import anyBSMPrinter
from anyBSM.utils import import_sympy
SM.sympify_parameters() # adds LaTeX strings and sympy symbols to the dictionaries `SM.texnames` and `SM.symbols` corresponding to the UFO parameters

# define custom printer
def latex(expr, **settings):
    sett = {'symbol_names': SM.texnames}
    sett.update(settings)                                      
    return anyBSMPrinter(sett).doprint(expr)
sp = import_sympy() # make sure to import sympy only once
sp.init_printing(latex_printer=latex) # initialize sympy printing
```
"""
