from os import path, getcwd, mkdir
from collections import defaultdict
from jinja2 import Template
from jinja2.filters import FILTERS
from shutil import which, copy2, SameFileError
import logging
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from anyBSM.utils import fieldtypes, module_dir
from anyBSM.latex.printer import latex, texname, line, particle_name
from sympy import sympify # TODO avoid imports everywhere

logger = logging.getLogger('anyBSM.latex.drawer')

__doc__ = """
# LaTeX Output
Generates LaTeX summary of all calculated diagrams using [TikZ-Feynman](https://www.sciencedirect.com/science/article/abs/pii/S0010465516302521)

## Example
from anyBSM import anyBSM
from anyBSM.latex.drawer import DrawProcess

model = anyBSM('THDMII')
h=model.SM_particles['Higgs-Boson']

# calculated tadpole and draws result
tad=model.process(h, draw=True)

# the following is equivalent to above but gives you access to the drawer
drawer = DrawProcess(model, externalfields=[h])
model.process(h, draw=drawer)
# here you could calculate/draw more diagrams
# finalize/compile the latex output
drawer.write(result=tad)

"""

drawer_path = path.join(module_dir, 'latex')

FILTERS['line'] = line
FILTERS['texname'] = texname

def printparameters(parameters):
    string = ''
    r = 7 # number of digits
    ncol = 5 # number of columns
    colsep = 'l'.join(['' for i in range(ncol+1)])
    nparas = len(parameters)
    string += f'\\begin{{longtable}}{{{colsep}}}\n'
    for i,p in enumerate(sorted(parameters, key=lambda x: x.name.lower())):
        num = p.nvalue
        try:
            if abs(num.imag) > r+2:
                num = str(round(num.real, r) + round(num.imag, r) * 1j)
            else:
                num = str(round(num.real, r))
            num = latex(sympify(num))
        except AttributeError:
            logger.warning(f'cannot latexify parameter value {p.name}={p.nvalue}')
            num = '\\text{NaN}'
        if p.name != 'ZERO':
            string += f'${p.texname} = {num}$'
            if (i+1) % ncol == 0:
                string += ', \\\\\n'
            elif (i+1) != nparas:
                string += ', & '
    string += '\\end{longtable}'
    return string


class DrawProcess():
    r""" Draw a list of Feynman diagrams along with their results.
    Upon initialization the header of the $\LaTeX$ file is written to the
    model directory. Each call of `DrawProcess.add_diagram(topo,
    particles, result)` registers a new diagram
    of topology type `topo` (c.f. `anyBSM.anyBSM.topolgies`) and internal particles `particles` as well
    as its analytical/numerical `result` to be written to the file.
    Calling `DrawProcess.write()` writes the individual results to the
    file as well as generates an overview which lists all insertions.
    """
    model: object
    """ The `anyBSM.anyBSM()` model object """
    externalfields: tuple
    """ List of external fields of the amplitude (`anyBSM.ufo.object_library.Particle` objects) """
    simplify: bool
    """ whether to simplify analytic results """
    cutoff: object
    """ Whether to place a `cutoff` (numerical value) on which diagrams to draw. `False`: no cutoff. """
    def __init__(self,model, externalfields, simplify = False, cutoff = False):
        self.file = path.join(model.modeldir,  'latex', model.name + '_' + ''.join(f.name for f in externalfields) + f'_{model.evaluation}_results.tex')
        if not path.exists(path.dirname(self.file)):
            mkdir(path.dirname(self.file))
        self.model = model
        self.ext = externalfields
        self.extnames = ','.join(particle_name(f) for f in externalfields)
        self.exttype = fieldtypes(externalfields)
        self.simplify = simplify
        self.cutoff = cutoff if cutoff is not True else False
        self.next = len(externalfields)
        self.insertions = defaultdict(dict)
        self.diagrams = defaultdict(dict)
        options = f'Cut-off set to: ${self._unit(cutoff)}$ (plotting only diagram with |result|$>{self._unit(cutoff)}$).' if self.cutoff else ''

        with open(self.file, 'w') as f:
            f.write(f"""
% MANUAL COMPILATION:
% lualatex --halt-on-error {path.basename(self.file)}
\\documentclass[11pt]{{article}}
\\usepackage[margin=2.5cm]{{geometry}}
\\usepackage{{amsmath}}
\\usepackage{{breqn}}
\\usepackage{{array}}
\\usepackage{{hyperref}}
\\usepackage{{ltablex}}
\\usepackage{{amssymb}}
\\usepackage{{tikz}}
\\usepackage[compat=1.1.0]{{{drawer_path}/tikzfeynman/tikzfeynman}}
\\usepackage{{array}}
\\usepackage{{longtable}}
\\usepackage{{units}}
\\begin{{document}}
\\newcolumntype{{L}}[1]{{>{{\\raggedleft\\arraybackslash}}m{{#1}}}}
\\title{{anyBSM - Model: {model.name} (Amplitude: ${'-'.join([particle_name(f) for f in self.ext])}$)}}
\\author{{Henning Bahl, Johannes Braathen, Martin Gabelmann, Georg Weiglein}}
\\maketitle
{options}
% \\tableofcontents % uncomment and compile twice for TOC
% \\pagebreak
""")

    def _unit(self,num = ''):
        """ returns the unit (in GeV) of the amplitude in LaTeX-form."""
        u = 4 - self.next
        u = '' if u == 1 else f'^{u}'
        if num:
            return f'\\unit[{num}]{{\\text{{GeV}}{u}}}'
        return f'\\text{{GeV}}{u}'

    def add_diagram(self, topo, particles, result):
        """ Register a diagram to draw.
            * `topo`: string that represents a topology defined in
            anyBSM.topologies
            * `particles`: list of
            `anyBSM.ufo.object_library.Particle()`
            * `result` numerical or analytical result of the diagram
            (number- or string-type)
        """
        if self.model.evaluation == 'numerical' and (self.cutoff and abs(result) < float(self.cutoff)):
            return
        inttype = fieldtypes(particles)
        if topo not in skeletons[self.next]:
            return
        if inttype not in self.insertions[topo]:
            self.insertions[topo][inttype] = [skeletons[self.next][topo].render(
                    external=self.ext,
                    internal=particles,
                    generic=True
                    )]
        if inttype:
            self.insertions[topo][inttype].append('\\{' + ','.join([particle_name(f) for f in particles]) + '\\}')

        if inttype not in self.diagrams[topo]:
            self.diagrams[topo][inttype] = []
        norm = '64*pi**2'
        normtex = ' $64\\pi^2\\times$ '
        if 'Tree' in topo or self.model.evaluation == 'numerical':
            norm = '1'
            normtex = ''

        result = '0' if result == '' else result
        if self.model.evaluation != 'numerical':
            result = self.model.sympify(f'{norm}*({result}+0)')
            result = latex(result, symbol_names = self.model.texnames)
        self.diagrams[topo][inttype].append([
            normtex,
            skeletons[self.next][topo].render(external=self.ext, internal=particles, generic=False),
            ' = & \\begin{dmath*}\n',
            result,
            '\n\\end{dmath*}\n \\\\'
        ])

    def write(self, result={}):
        """ Writes all registered diagrams to the latex file and try to
        compile it.
          * `result`: the result of `anyBSM.process()` i.e. a
          dictionary separating the summed results of the individial
          topologies.

        At the beginning of the file, an overview with all insertions
        for the various topologies is generated. If the numerical
        evaluation mode is used and `result` is given, an overview of the different
        contributions and their weights is listed.
        """
        f = open(self.file, 'a')
        f.write('\n\n\\section{Overview}\n')
        for topo in self.insertions:
            f.write(f'\\subsection{{Topology: {topo}}}\n\n')
            f.write('\\begin{tabularx}{\\textwidth}{@{}rlX@{}}')
            for inttype,ins in self.insertions[topo].items():
                f.write(ins[0])
                if inttype:
                    f.write('& $\\{' + ','.join(f for f in inttype) + '\\} =$ &')
                    f.write('$' + '$, $'.join(ins[1:min(len(ins), 50)]) + '$')
                    if len(ins) > 50:
                        f.write(f' (+{len(ins)-50} more insertions) \\\\ \n')
                    else:
                        f.write('\\\\ \n')
                else:
                    f.write('& & \\\\\n')
            f.write('\\end{tabularx}\n')
        if self.model.evaluation == 'numerical' and result:
            f.write('\n\\section{Numerical input values}\n')
            f.write('\n\\subsection{Input (external) parameters}\n')
            f.write(printparameters(self.model.external_parameters))
            f.write('\n\\subsection{Derived (internal) parameters}\n')
            f.write(printparameters(self.model.internal_parameters))
            result = dict(result)
            f.write('\n\\section{Summary of individual results}\n')
            f.write('\n\\textit{Relative (\\%) values are calculated for real parts only.}\n\n')
            f.write("""
                    \\begin{itemize}
                    \\item see appendix A.2 of arXiv:2305.03015 for an explanation of the different topologies,
                    \\item ThreePointTree corresponds to the tree-level result,
                    \\item the sum of ThreePointB and ThreePointC corresponds to the genuine 1-loop result,
                    \\item the sum of ThreePointTA and ThreePointWFRT corresponds to the 1-loop tadpole contribution,
                    \\item the sum of ThreePointWFRA and ThreePointWFRB corresponds to the 1-loop WFR contribution,
                    \\item \\textbf{counterterm contributions are not included in these results.}
                    \\end{itemize}\n\n""")
            for k,v in result.items():
                result[k] = eval(str(v))
                if 'ThreePoint' in k:
                    result[k] = - result[k]
            total = sum(eval(str(r)) for r in result.values())
            f.write('\\begin{align*}')
            f.write('\\textbf{Topology} & & \\textbf{contribution in ' + self._unit() + '} & & \\textbf{in \\%} \\\\ \\cline{1-5} \n')
            f.write(f'\\text{{Sum of contributions}} & & {self._unit(total)} & & \\textbf{{(100\\%}})\\\\ \n')
            for k,v in result.items():
                f.write(f'\\text{{{k}}} & & {self._unit(result[k])} & & \\textbf{{({round(100*result[k].real/total.real,3)}\\%}})\\\\ \n')
            f.write('\\end{align*}\n')
        f.write('\n\\section{Individual results}\n')
        for topo in self.diagrams:
            f.write(f'\\subsection{{Topology: {topo}}}\n')
            for inttype, diags in self.diagrams[topo].items():
                f.write(f'\\subsubsection{{{inttype}}}\n')
                f.write('\\begin{longtable}{rL{0.9\\textwidth}}')
                for diag in diags:
                    if self.model.evaluation == 'numerical' and abs(total) > 0:
                        diag[3] = self._unit(latex(sympify(diag[3]))) + ' \\quad \\textbf{(' + str(round(diag[3].real*100/total.real,3)) + '\\%)}'
                    else:
                        diag[3] = str(diag[3])
                    f.write(''.join(diag) + '\n')
                f.write("\n\\end{longtable}\n")
        f.write("\n\\vfill\n\\textit{This document was compiled with the help of \\href{https://www.sciencedirect.com/science/article/abs/pii/S0010465516302521}{TikZ-Feynman}}")
        f.write("\\end{document}")
        f.close()
        lualatex = which('lualatex') or which('pdflatex')
        if not lualatex:
            logger.error('Cannot find any lualatex/pdflatex installation on your system.')
            return
        print(f"Compiling LaTeX ({self.file})...")
        proc = Popen(
                [lualatex, '--halt-on-error', self.file],
                stderr=STDOUT,
                stdout=PIPE,
                cwd=path.dirname(self.file)
        )
        try:
            stdout, stderr = proc.communicate(timeout=600)
            rc = proc.poll()
            fname = path.splitext(self.file)[0] + '.pdf'
            if rc != 0 or not path.exists(fname):
                logger.error('LaTeX compilation failed:')
                return
            print("done.")
            newpath = path.abspath(path.join(getcwd(), path.basename(fname)))
            try:
                copy2(fname, newpath)
            except SameFileError:
                pass
            print(f"Open the pdf file at: {newpath}")
        except TimeoutExpired:
            logger.error(f"Compiling LaTeX failed (timeout). Please try manually compiling {self.file}")
            proc.kill()


skeletons = defaultdict(dict)
""" skeletons[number_external_legs][topology_name] (identical to anyBSM.topologies.TOPOLOGIES)
contains Template expressions for Feynman diagrams of the different
topologies.
"""

skeletons[1]['OnePointA'] = Template(r"""
\begin{tikzpicture}[baseline=0]
    \begin{feynman}
        \vertex (in){${{ external[0]|texname(generic, True) }}$};
        \vertex[right=1.0cm of in](a);
        \vertex[right=1.5cm of a](b);
        \vertex[right=0.8cm of a](label) {${{ internal[0]|texname(generic) }}$};
        \vertex[right=0.6cm of b](tmo) {};
        \diagram*{(in) -- [{{external[0]|line}}] (a), (a) --[{{internal[0]|line}}, half right] (b) -- [{{internal[0]|line}}, half right] (a)};
    \end{feynman}
\end{tikzpicture}

""")

skeletons[2]['TwoPointA'] = Template(r"""
\begin{tikzpicture}[baseline=0]
    \begin{feynman}
        \vertex (in){${{ external[0]|texname(generic, True) }}$};
        \vertex[right=1.5cm of in](a);
        \vertex[above=1.5cm of a](b);
        \vertex[right=1.1cm of a](out) {${{ external[1]|texname(generic, True) }}$};
        \vertex[above=0.8cm of a](label) {${{ internal[0]|texname(generic) }}$};
        \diagram*{(in) -- [{{external[0]|line}}] (a), (a) --[{{external[1]|line}}] (out), (a) -- [{{internal[0]|line}}, half right] (b) -- [{{internal[0]|line}}, half right] (a)};
    \end{feynman}
\end{tikzpicture}

""")

skeletons[2]['TwoPointB'] = Template(r"""
\begin{tikzpicture}[baseline=0]
    \begin{feynman}
        \vertex (in) {${{ external[0]|texname(generic,True) }}$};
        \vertex[right=1cm of in](a);
        \vertex[right=1.5cm of a](b);
        \vertex[right=0.6cm of b](out) {${{ external[1]|texname(generic, True) }}$};
        \diagram*{(in)  -- [{{external[0]|line}}] (a), (b) -- [{{external[1]|line}}] (out),
                  (a)  -- [{{internal[0]|line}}, edge label=${{internal[0]|texname(generic)}}$,half left,looseness=1.59] (b),
                  (b)  -- [{{internal[1]|line}}, edge label=${{internal[1]|texname(generic)}}$,half left,looseness=1.59] (a)
                 };
    \end{feynman}
\end{tikzpicture}

""")

skeletons[2]['TwoPointTA'] = Template(r"""
\begin{tikzpicture}[baseline=0]
    \begin{feynman}
        \vertex (in){${{ external[0]|texname(generic, True) }}$};
        \vertex[right=1.5cm of in](a);
        \vertex[above=1cm of a](b);
        \vertex[right=1.1cm of a](out) {${{ external[1]|texname(generic, True) }}$};
        \vertex[above=0.8cm of a](label) {};
        \diagram*{(in) -- [{{external[0]|line}}] (a),
                  (a) --[{{external[1]|line}}] (out),
                  (a) -- [{{internal[0]|line}}, edge label=${{ internal[0]|texname(generic) }}$] (b)};
        \draw[{{internal[1]|line}}] (b) arc [start angle=-90, end angle=270, radius=0.5cm] node[label=${{internal[1]|texname(generic)}}$] {};
    \end{feynman}
\end{tikzpicture}

""")

skeletons[3]['ThreePointTree'] = Template(r"""
\begin{tikzpicture}[baseline=0]
    \begin{feynman}
        \vertex (X);
        \vertex[left=1cm of X] (e1) {${{ external[0]|texname(generic,True) }}$};
        \vertex[right=1cm of X] (tmp);
        \vertex[above=1cm of tmp] (e2) {${{ external[1]|texname(generic,True) }}$};
        \vertex[below=1cm of tmp] (e3) {${{ external[2]|texname(generic,True) }}$};
        \diagram*{(e1)  -- [{{external[0]|line}}] (X),
                  (X)  -- [{{external[1]|line}}] (e2),
                  (X)  -- [{{external[2]|line}}] (e3)};
    \end{feynman}
\end{tikzpicture}

""")

skeletons[3]['ThreePointB'] = Template(r"""
\begin{tikzpicture}[baseline=0]
    \begin{feynman}
        \vertex (in) {${{ external[0]|texname(generic,True) }}$};
        \vertex[right=1cm of in](a);
        \vertex[right=1.5cm of a](b);
        \vertex[right=1cm of b](tmp);
        \vertex[above=0.56cm of tmp](out1) {${{ external[1]|texname(generic, True) }}$};
        \vertex[below=0.56cm of tmp](out2) {${{ external[2]|texname(generic, True) }}$};
        \diagram*{(in)  -- [{{external[0]|line}}] (a),
                  (b) -- [{{external[1]|line}}] (out1),
                  (b) -- [{{external[2]|line}}] (out2),
                  (a)  -- [{{internal[0]|line}}, edge label=${{internal[0]|texname(generic)}}$,half left,looseness=1.59] (b),
                  (b)  -- [{{internal[1]|line}}, edge label=${{internal[1]|texname(generic)}}$,half left,looseness=1.59] (a)
                 };
    \end{feynman}
\end{tikzpicture}

""")

skeletons[3]['ThreePointC'] = Template(r"""
\begin{tikzpicture}[baseline=(a)]
    \begin{feynman}
      \vertex at (0,1.75) (a) {${{ external[1]|texname(generic,True) }}$};
      \vertex at (3.5,0) (b) {${{ external[2]|texname(generic,True) }}$};
      \vertex at (3.5,3.5) (c) {${{ external[0]|texname(generic,True) }}$};

      \vertex at (1.16,1.75) (a1);
      \vertex at (2.62,0.58) (b1);
      \vertex at (2.62,2.917) (c1);

      \diagram* {
      (a) -- [{{external[1]|line}}] (a1),
      (b) -- [{{external[2]|line}}] (b1),
      (c) -- [{{external[0]|line}}] (c1),
      (a1) -- [{{internal[0]|line}}, edge label=${{internal[0]|texname(generic)}}$] (c1) -- [{{internal[1]|line}}, edge label=${{internal[1]|texname(generic)}}$] (b1) -- [{{internal[2]|line}}, edge label=${{internal[2]|texname(generic)}}$] (a1)
      };

    \end{feynman}
\end{tikzpicture}

""")

skeletons[3]['ThreePointTA'] = Template(r"""
\begin{tikzpicture}[baseline=(X.base)]
    \begin{feynman}
        \vertex (X);
        \vertex[left=1cm of X] (t1);
        \vertex[right=0.5cm of X] (t2);
        \vertex[right=1cm of X] (t3);
        \vertex[above=1cm of t1] (e1) {${{ external[0]|texname(generic,True) }}$};
        \vertex[below=1cm of t1] (e2) {${{ external[1]|texname(generic,True) }}$};
        \vertex[below=1cm of t3] (e3) {${{ external[2]|texname(generic,True) }}$};
        \vertex[above=0.5cm of t2] (x);
        \diagram*{(e1)  -- [{{external[0]|line}}] (X),
                  (e2)  -- [{{external[1]|line}}] (X),
                  (X)  -- [{{external[2]|line}}] (e3),
                  (X)  -- [{{internal[0]|line}}, edge label=${{internal[0]|texname(generic)}}$] (x)};
        \draw[{{internal[1]|line}}] (x) arc [start angle=-135, end angle=225, radius=0.55cm] node[label=20:${{internal[1]|texname(generic)}}$] {};
    \end{feynman}
\end{tikzpicture}

""")

skeletons[3]['ThreePointWFRA'] = Template(r"""
\begin{tikzpicture}[baseline=(X.base)]
    \begin{feynman}
        \vertex (X);
        \vertex[left=1cm of X] (e1) {${{ external[0]|texname(generic,True) }}$};
        \vertex[right=1cm of X] (tmp);
        \vertex[right=0.5cm of X] (tmp0);
        \vertex[above=0.5cm of tmp0] (x);
        \vertex[above=1cm of tmp] (e2) {${{ external[2]|texname(generic,True) }}$};
        \vertex[below=1cm of tmp] (e3) {${{ external[1]|texname(generic,True) }}$};
        \diagram*{(e1)  -- [{{external[0]|line}}] (X),
                  (X)  -- [{{external[2]|line}}] (e3),
                  (X)  -- [{{internal[0]|line}}, edge label'=${{internal[0]|texname(generic)}}$] (x),
                  (x)  -- [{{external[1]|line}}] (e2)};
        \draw[{{internal[1]|line}}] (x) arc [start angle=-45, end angle=315, radius=0.4cm] node[label={[xshift=-0.5cm,yshift=0.5cm]${{internal[1]|texname(generic)}}$}] {};
    \end{feynman}
\end{tikzpicture}

""")

skeletons[3]['ThreePointWFRB'] = Template(r"""
\begin{tikzpicture}[baseline=(X.base)]
    \begin{feynman}
        \vertex (X);
        \vertex[left=1cm of X] (e1) {${{ external[0]|texname(generic,True) }}$};
        \vertex[right=1.5cm of X] (tmp);
        \vertex[right=0.5cm of X] (tmp0);
        \vertex[right=1cm of X] (tmp1);
        \vertex[above=0.5cm of tmp0] (x1);
        \vertex[above=1cm of tmp1] (x2);
        \vertex[above=1.3cm of tmp] (e2) {${{ external[2]|texname(generic,True) }}$};
        \vertex[below=1.3cm of tmp] (e3) {${{ external[1]|texname(generic,True) }}$};
        \diagram*{(e1)  -- [{{external[0]|line}}] (X),
                  (X)  -- [{{external[2]|line}}] (e3),
                  (X)  -- [{{internal[0]|line}}, edge label=${{internal[0]|texname(generic)}}$] (x1),
                  (x1)  -- [{{internal[1]|line}}, edge label=${{internal[1]|texname(generic)}}$, half left] (x2),
                  (x2)  -- [{{internal[2]|line}}, edge label=${{internal[2]|texname(generic)}}$, half left] (x1),
                  (x2)  -- [{{external[1]|line}}] (e2)};
    \end{feynman}
\end{tikzpicture}

""")
skeletons[3]['ThreePointWFRT'] = Template(r"""
\begin{tikzpicture}[baseline=(X.base)]
    \begin{feynman}
        \vertex (X);
        \vertex[left=1cm of X] (e1) {${{ external[0]|texname(generic,True) }}$};
        \vertex[right=1cm of X] (tmp);
        \vertex[right=0.5cm of X] (tmp0);
        \vertex[above=0.57cm of tmp0] (x);
        \vertex[left=0.25cm of X] (tmp1);
        \vertex[left=0.75cm of x] (tmp2);
        \vertex[above=1cm of tmp] (e2) {${{ external[2]|texname(generic,True) }}$};
        \vertex[below=1cm of tmp] (e3) {${{ external[1]|texname(generic,True) }}$};
        \diagram*{(e1)  -- [{{external[0]|line}}] (X),
                  (X)  -- [{{external[2]|line}}] (e3),
                  (X)  -- [{{internal[0]|line}}, edge label'=${{internal[0]|texname(generic)}}$] (x),
                  (x)  -- [{{internal[1]|line}}, edge label'=${{internal[1]|texname(generic)}}$] (tmp2),
                  (x)  -- [{{external[1]|line}}] (e2)};
        \draw[{{internal[2]|line}}] (tmp2) arc [start angle=0, end angle=360, radius=0.3cm] node[label={[xshift=-1.0cm,yshift=-0.3cm]${{internal[2]|texname(generic)}}$}] {};
    \end{feynman}
\end{tikzpicture}

""")

skeletons[3]['ThreePointCT'] = Template(r"""
\begin{tikzpicture}[baseline=0]
    \begin{feynman}
        \vertex[crossed dot] (X) {};
        \vertex[left=1cm of X] (e1) {${{ external[0]|texname(generic,True) }}$};
        \vertex[right=1cm of X] (tmp);
        \vertex[above=1cm of tmp] (e2) {${{ external[1]|texname(generic,True) }}$};
        \vertex[below=1cm of tmp] (e3) {${{ external[2]|texname(generic,True) }}$};
        \diagram*{(e1)  -- [{{external[0]|line}}] (X),
                  (X)  -- [{{external[1]|line}}] (e2),
                  (X)  -- [{{external[2]|line}}] (e3)};
    \end{feynman}
\end{tikzpicture}

""")

skeletons[3]['ThreePointMCT'] = Template(r"""
\begin{tikzpicture}[baseline=0]
    \begin{feynman}
        \vertex (X);
        \vertex[left=0.5cm of X] (tmp);
        \vertex[crossed dot, above=0.5cm of tmp] (ct) {};
        \vertex[left=1cm of X] (e1) {${{ external[0]|texname(generic,True) }}$};
        \vertex[right=1cm of X] (tmp);
        \vertex[above=1cm of tmp] (e2) {${{ external[1]|texname(generic,True) }}$};
        \vertex[below=1cm of tmp] (e3) {${{ external[2]|texname(generic,True) }}$};
        \diagram*{(e1)  -- [{{external[0]|line}}] (X),
                  (X)  -- [{{external[1]|line}}] (e2),
                  (X)  -- [{{external[2]|line}}] (e3)};
    \end{feynman}
\end{tikzpicture}

""")
