from tqdm.auto import tqdm
from pandas import DataFrame
import matplotlib
import matplotlib.axes
import numpy as np
from numpy.random import default_rng
from PIL import Image
from os import path
from anyBSM import anyBSM
from anyBSM.utils import module_dir

__doc__ = """# AnyPlot
A module to set default matplotlib-styles, perform simple random- and grid-scans with anyBSM as well as to plot the results.
"""

default_labels = {
    'kappalambda' : '$\\kappa_\\lambda$',
    'total' : '$\\lambda^{\\mathrm{NLO}} \\,\\, \\mathrm{GeV}$',
    'treelevel' : '$\\lambda^{\\mathrm{LO}} \\,\\, \\mathrm{GeV}$',
    'eig0' : '$|a_{J=0}^{\\mathrm{max}}|$',
}
""" LaTeX representation of quantities that most likely appear on one
of the axes but do not happen to be defined in UFO """

logo_path = path.join(module_dir, 'logos')

anyLogo = {'resize': False, 'show': True, 'alpha': 0.5, 'zorder': 0, 'loc': 'lower right'}
""" Default values for the anyH3 logo which is automatically added to all matplotlib axes/plots.
`show` may be boolean or a list of integers marking the subplots which shall contain the logo.
"""

def logo(resize=False, logo_name = None):
    """ load logo and optionally resize it. Return logo PIL object """
    size = resize or anyLogo.get('resize', False)
    logoname = logo_name if logo_name else anyLogo.get('logo_name', 'anyH3_logo_plot.png')
    img = Image.open(path.join(logo_path, logoname))
    if size:
        img = img.resize(
            (int(size*img.size[0]),int(size*img.size[1])),
            Image.LANCZOS)
    return img

def place_logo(fig,x=0.9,y=0.69,resize=False,logo_name='anyH3_logo_plot.png',**kwargs):
    """ place logo manually to a given figure.

    It is imortant to set the figure dpi before calling this function
    and further to set the dpi size in `savefig`.
    Example:
    ```python
    fig, ax = plt.subplots()
    fig.dpi = 600
    # do your plotting here
    plotting.place_logo(fig,0.92,0.75, alpha=0.4,logo_name='anyH3_logo_small.png')
    fig.savefig('file.pdf', bbox_inches='tight',dpi=fig.dpi)
    ```
    """
    img = logo(resize=resize, logo_name=logo_name)
    if isinstance(fig, matplotlib.figure.FigureBase):
        return fig.figimage(
                img,
                x*fig.dpi*fig.get_figwidth(),
                y*fig.dpi*fig.get_figheight(),
                **kwargs)
    else:
        return img

class anyAxes(matplotlib.axes.Axes):

    """ Inherits/overwrites `matplotlib.axes.Axes` and adds the anyH3 logo to the Axes.
    The behaviour/styling of the logo can be changed using `anyBSM.anyBSM.plotting.anyLogo`.
    Alternatively use `plotting.place_logo` to place the logo manually.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if anyLogo.get('show', True) is False :
            return
        disable = anyLogo.get('show', [])
        disable = [] if disable is True else disable
        if disable and hasattr(args[1],'num1') and args[1].num1 not in disable:
            return

        img = logo()
        if isinstance(anyLogo['loc'], (list,tuple)) and hasattr(args[0],'figimage'):
            args[0].figimage(img, *anyLogo['loc'], alpha=anyLogo['alpha']) # manual placement
            return
        img_box = matplotlib.offsetbox.OffsetImage(img,alpha=anyLogo.get('alpha',0.5),dpi_cor = False)
        img_anchored = matplotlib.offsetbox.AnchoredOffsetbox(
                  anyLogo.get('loc', 'lower right'),
                  child = img_box,
                  frameon=False,
                  borderpad=0)
        img_anchored.set_zorder(anyLogo.get('zorder', 0))
        self.add_artist(img_anchored)

matplotlib.axes.Axes = anyAxes

import matplotlib.pyplot as plt # noqa: E402
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['xtick.top']   = True
matplotlib.rcParams['ytick.right'] = True
matplotlib.rcParams['xtick.minor.visible'] = True
matplotlib.rcParams['ytick.minor.visible'] = True
matplotlib.rcParams['xtick.direction'] = 'in'
matplotlib.rcParams['ytick.direction'] = 'in'
matplotlib.rcParams["xtick.minor.visible"] = True
matplotlib.rcParams["ytick.minor.visible"] = True
matplotlib.rcParams['font.size']   = 16.0
matplotlib.rcParams['font.family'] = 'serif'

def setAnyStyle(style='paper'):
    if style == 'paper':
        matplotlib.rcParams['font.family'] = 'serif'
    if style == 'beamer':
        matplotlib.rcParams['font.size']   = 18.0

class ScanParameter():
    def __init__(self, parameter, distribution = 'uniorm', *args, **kwargs):
        """ Defines a scan parameter.
          * `parameter`: anyBSM.ufo.object_library.Parameter()-object,
          i.e. any parameter defined in the UFO model
          * `distribution`: generator used in
          numpy.random.default_rng instance. Special value 'grid' is
          used to use `np.linspace` instead (in which case the kwargs
          'start' and 'stop' are required)
          * `*args`/`**kwargs` additional arguments passed to the
          generator (e.g. 'start' and 'stop' etc)
        """

        self.name = parameter.name
        self.tex = parameter.texname
        self.distribution = distribution
        self.values = []
        """ Store for the generated values """
        self.args = args
        self.kwargs = kwargs

    def generate(self, rng, n):
        """ Generate `n` random values using the generator instance
        `rng`. In case of `distribution=grid` was used, `np.linspace`
        is issued instead."""
        self.kwargs['size'] = n
        if self.distribution == 'grid':
            self.values = np.linspace(self.kwargs['start'], self.kwargs['stop'], num = n)
            return
        self.values = getattr(rng, self.distribution)(*self.args, **self.kwargs)

class Plotting():
    def __init__(self,model,lambdaSM=187.28177740658242, caching = 2, **kwargs):
        """ Perform scans using pre-defined scan parameter(ranges)
        (i.e. `ScanParameter`s).\n
         * `model`: anyBSM object
         * `lambdaSM`: normalization value for
         $\\kappa_\\lambda$-plots"""
        if not lambdaSM:
            print('calculating lambda_hhh^tree in the SM"')
            SM = anyBSM('SM',
                       progress=False,
                       quiet=True,
                       scheme_name='MS',
                       evaluation='numerical')
            SM.setparameters()
            self.lamSM = complex(0,1)*SM.getcoupling('h','h','h')['c'].nvalue
            print(f'    \\lambda_hhh^SM = {self.lamSM}')
        else:
            self.lamSM = lambdaSM

        self.model = model
        self.model.caching = caching
        model.evaluation = 'numerical'
        model.progress = False
        model.quiet = True

        self.rng = default_rng()

        self.results = {}

        setAnyStyle()

    def RandomScan(self, name = '', n = 0, parameters = [], **kwargs):
        """ Perform a random `anyBSM.lambdahhh()`-scan using a given list of scan
        `parameters` (while all other parameters are taken to be the
        default values from the UFO model). The scan runs until `n` samples have been
        calculated.
         * `name`: name of the scan
         * `n`: size of the scan sample
         * `parameters`: list of ScanParameter() objects
         * `kwargs`: passed to `anyBSM.anyBSM.lambdahhh(**kwargs)`
        The scan result is saved in a Pandas DataFrame
        `self.results[name]` and can be used/plotted with the
        `Scatter()` method.
        """
        if not name:
            name = f'scan_{len(self.results)}'
        if name in self.results:
            return self.results[name]
        for p in parameters:
            p.generate(self.rng, n)
        tmp = []
        for i in tqdm(range(n)):
            paras = {p.name: p.values[i] for p in parameters}
            self.model.setparameters(paras)
            res = self.model.lambdahhh(**kwargs)
            for k,v in res.items():
                paras.update({f'lambdahhh{k}': v})
            paras.update({'kappalambda': res['total'].real/self.lamSM, 'eig0': self.model.eigSSSS()})
            tmp.append(paras)
        self.results[name] = DataFrame(tmp)
        return self.results[name]

    def XY(self, scanpara, resultspara, n, parameters ={},lambdahhh_kwargs={}, *args, **kwargs):
        """ Perform a linear `anyBSM.lambdahhh()`-scan by varying on
        `ScanParameter()` `scanpara` and plot it against
        `resultspara`:
         * `scanpara`: a `ScanParameter()` object
         * `resultspara`: a string representing a column of the
         resulting DataFrame of the scan
         * `n`: number of points to plot
         * `parameters`: additional parameters to set; passed to
         `anyBSM.anyBSM.setparameters()`
         * `lambdahhh_kwargs`: arguments passed to anyH3.lambdahhh()
         * `*args/**kwargs`: additional arguments passed to
         `matplotlib.pyplot.plot`
        The `resultspara` value can be `lambdahhh` or 'kappalambda'. In
        addition, the individual contributions to lambdahhh
        {tree-level, genuine,WFRs,tadpoles,massCTs,VEVCT,customCT} are
        available via `lambdahhh{0,1,2,3,4,5,6}`.\n
        Example:
        ```python
        # here `SM` is the anyBSM model object
        MH = ScanParameter(SM.parameters['Mh'], distribution='grid',start = 10, stop = 500)
        plot = Plotting(SM)
        plot.XY(MH,'kappalambda', 20, parameters = {'Mu3': 173}, label='$M_{top}= 173$ GeV')
        plot.XY(MH,'kappalambda', 20, parameters = {'Mu3': 150}, label='$M_{top}= 150$ GeV')
        ```
        """
        tmp = []
        self.model.setparameters(parameters)
        scanpara.generate(self.rng, n)
        for i in range(n):
            paras = dict(parameters)
            paras = {scanpara.name: scanpara.values[i]}
            self.model.setparameters(paras)
            res = self.model.lambdahhh(**lambdahhh_kwargs)
            for k,v in res.items():
                paras.update({f'lambdahhh{k}': v})
            paras.update({'kappalambda': res['total'].real/self.lamSM, 'eig0': self.model.eigSSSS()})
            tmp.append(paras)
        df = DataFrame(tmp)
        p = plt.plot(df[scanpara.name], df[resultspara], *args, **kwargs)
        ylabel = default_labels.get(resultspara, resultspara)
        plt.xlabel(f'${scanpara.tex}$')
        plt.ylabel(ylabel)
        return p

    def Scatter(self, name, parameter_x, parameter_y, colorbar_kwargs = {}, *args, **kwargs):
        """ Plot the 2(3)-dimensional hypersphere of the result of a previous
        N-dimensional random scan `name` performed with `RandomScan(name=name)`.
         * `name`: name of the scan; stored in the DataFrame self.results[name]
         * `parameters_x`: parameter/column from the DataFrame to be
         plotted on the x-axis
         * `parameters_y`: parameter/column from the DataFrame to be
         plotted on the y-axis
         * `*args/*kwargs`: additional arguments for
         matplotlib.pyplot.scatter such as e.g. `c='kappalambda' to
         automatically  introduce a heat-map and add a colorbar with
         the label $\\kappa_\\lambda$`.\n
        Example:
        ```python
        plot = Plotting(SM)
        MT = ScanParameter(SM.parameters['Mu3'], distribution='uniform', low = 150, high = 180)
        MH = ScanParameter(SM.parameters['Mh'] , distribution='uniform', low = 100, high = 300)
        plot.RandomScan(name = 'MTMHScan', parameters = [MT,MH], n = 500)
        p = plot.Scatter('MTMHScan',MH,MT, c='kappalambda')
        ```
        """
        self.model.setparameters()
        if name not in self.results:
            print(f'cant find results for scan "{name}"')
            return
        df = self.results[name]
        if 'c' in kwargs and type(kwargs['c']) == str:
            clabel = default_labels.get(kwargs['c'], kwargs['c'])
            kwargs['c'] = df[kwargs['c']]
        else:
            clabel = kwargs['c']

        p = plt.scatter(df[parameter_x.name], df[parameter_y.name], *args, **kwargs)
        xlabel = parameter_x.tex.replace('text', 'rm')
        ylabel = parameter_y.tex.replace('text', 'rm')
        plt.xlabel(fr'${xlabel}$')
        plt.ylabel(fr'${ylabel}$')
        cbar = None
        if 'c' in kwargs:
            cbar = plt.colorbar(p, **colorbar_kwargs)
            cbar.set_label(clabel)
        fig = plt.gcf()
        return [fig, cbar]
