import numpy as np
import numpy.matlib

from controls import ValueControl
from controls import OptionSelect
from fractal import Fractal
import utils


class Function(object):
    """Represents a mathematical function."""

    # Static constants.
    FUNCTIONS = []
    _ID = 0

    def __init__(self, name, func, deriv):
        self.name = name
        self._f = func
        self._df = deriv

        # Keep static reference to this Function instance.
        Function.FUNCTIONS.append(self)
        Function._ID += 1

    def __call__(self, *args):
        return self._f(*args)

    def newtonsMethod(self, x, a):
        """Approximates root of this function using single iteration of 
           Newton's method.
        """
        return x - a * (self._f(x) / self._df(x))


SIN = Function(
    "Sin",
    func=np.sin,
    deriv=np.cos
)
COS = Function(
    "Cosine",
    func=np.cos,
    deriv=lambda x: -1 * np.sin(x)
)
TRIG1 = Function(
    "Composite Trig",
    func=lambda x: np.cos(np.sin(x)) - np.pi,
    deriv=lambda x: -1 * np.cos(x) * np.sin(np.sin(x))
)
POLY1 = Function(
    "Polynomial",
    func=lambda x: np.power(x, 3) + 1,
    deriv=lambda x: 3 * np.power(x, 2)
)


def getFunction(funct_id):
    return Function.FUNCTIONS[funct_id]


def getFunctions():
    return Function.FUNCTIONS


class Newton(Fractal):

    def _computeFractal(self, complex_plane, itermax, f=TRIG1, a=1.0, e=0.001):
        z = complex_plane

        # Matrix of number of iterations required to reach solution.
        root_iters = np.matlib.zeros(z.shape)

        for i in xrange(itermax):
            z = f.newtonsMethod(z, a)

            # Increment points where solutions have been found.
            roots = np.where(abs(f(z)) < e)
            root_iters[roots] += 1

        return [z.real, z.imag, root_iters]

    def _toRgbImage(self, fractal, colors, color_offset):
        """
        Convert the generated fractal into an RGB image array.

        :param colors: Number of colors permitted in image
        :param color_offset: Default offset for generating color hues
        :return: ndarry of shape (n, m, 3)
        """
        soln_real = utils.adjustRange(fractal[0], 0, 127)
        soln_imag = utils.adjustRange(fractal[1], 0, 127)
        iters = utils.adjustRange(fractal[2], 0, 128)

        rgb_image = np.array([
                soln_real + iters,
                soln_imag + iters,
                iters
            ]
        ).astype(dtype=np.uint8)

        return rgb_image.T

    def _createControls(self):
        """Create UI for editing fractal generation parameters."""
        a_control = ValueControl("a", vmin=-2, vmax=3, default=2, precision=2)
        e_control = ValueControl("e", vmin=0.00001, vmax=1, default=2, precision=5)
        f_control = OptionSelect("f", SIN, Function.FUNCTIONS)

        self.controls.addControl("Initial Value", a_control)
        self.controls.addControl("Root Approximation", e_control)
        self.controls.addControl("Function", f_control)
