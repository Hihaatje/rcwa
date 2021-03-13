__version__ = '0.0.1'
__author__ = 'Jordan Edmunds'
__email__ = 'edmundsj@uci.edu'
import os

file_location = os.path.dirname(__file__)
nkLocation = os.path.join(file_location, 'nkData/')

from rcwa.source.material import Material
from rcwa.source.crystal import Crystal
from rcwa.source.layer import LayerStack, Layer
from rcwa.source.source import Source, zeroSource
from rcwa.source.solver import Solver
from rcwa.source.plotter import Plotter
