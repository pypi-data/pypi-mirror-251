from collections import Counter
from os import path
import sys
import importlib.util
import logging
import pylha

__doc__ = """ # AnyUtility
A module to store all kinds of useful functions used accross different modules.
"""

spintypes = {-1: 'U', 1 : 'S', 2 : 'F', 3 : 'V'}
""" Mapping between UFO integers representing spins and internal field strings """
typesspin = {'U': -1, 'S': 1, 'F': 2, 'V': 3}
""" Inverse of `spintypes` """

def fieldtypes(fieldlist, sort = False):
    """ Take a list of UFO particle objects, `anyBSM.ufo.object_library.Particle()`,
    and returns a string with the corresponding field types.
     * `sort`: whether to sort the field types before concatenating them
    Examples:
     * `fieldtypes([3,3,1])` yields "VVS"
     * `fieldtypes([3,3,2], sort=True)` yields "SVV"
    """
    types = [spintypes.get(f.spin, 'UNKOWN') for f in fieldlist]
    if sort:
        types.sort()
    return ''.join(types)

def fieldcount(fieldlist):
    """ Returns `collections.Counter()` yielding
    how often a field is contained in a list """
    return Counter([p.name for p in fieldlist])

module_dir = path.abspath(path.dirname(__file__))
""" Path to anyBSM installation """

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        choice = input(question + " (respond with 'yes' or 'no' or 'y' or 'n') " + prompt).lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]

def import_sympy():
    """ Importing sympy can by quite expensive. Furthermore, we want
    to preserve global options set in sympy across different modules.
    This function checks if sympy was already imported (via
    `sys.modules`) and returns the existing package instead.\n
    Usage: `sp = import_sympy()`"""
    if 'sympy' not in sys.modules:
        import sympy # noqa: F401
    return sys.modules['sympy']

class LHA():
    """ A simple (S)LHA parser pased on
    [pylha](https://github.com/DavidMStraub/pylha)"""
    def __init__(self,file):
        """ `file`: path to the (S)LHA file to load` """
        try:
            with open(file,'r') as f:
                lha = pylha.load(f)
        except FileNotFoundError:
            logging.error(f'File {file} not found.')
            return {}
        if 'BLOCK' not in lha:
            logging.warning(f'No (S)LHA blocks defined in {file}')
            return None
        self.blocks = {k.upper():v for k,v in lha['BLOCK'].items()}
        self.blocks['DECAY'] = lha.get('DECAY', {})
        self.file = file

    def get(self, lha_block, lha_code):
        """ Return the value from `lha_block` (string) at position
        `lha_code` (list of integers).\n `
        """
        try:
            block = self.blocks[lha_block.upper()]
        except KeyError:
            logging.error(f'LHA block {lha_block} not found in {self.file}')
            return 0
        if lha_block == 'DECAY':
            pid = str(lha_code[0])
            # return total width
            try:
                return self.blocks['DECAY'][pid]['info'][0]
            except KeyError:
                logging.warning(f'Decay for PID {pid} not found in {self.file}')
                return
        block = block['values']
        size = len(lha_code)
        for entry in block:
            if entry[:size] == lha_code:
                if len(entry[size:]) == 1:
                    return entry[size]
                return entry[size:]
        logging.error(f'LHA block {lha_block} in {self.file} does not contain the entry {lha_code}')
        return 0

def lazy_import(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
