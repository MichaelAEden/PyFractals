from abc import abstractmethod, ABCMeta

import numpy as np
import numpy.matlib

import pylab

class Fractal(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = None

    def get_complex_plane(self, n, m, xmin, xmax, ymin, ymax):
        """Returns a matrix representing the complex plane."""

        # Creates two matrices of size n x m
        ix, iy = np.mgrid[0:n, 0:m]

        # Here we create a range of values in the x- and y-axis, then multiply by the matrices created before
        real_part = np.linspace(xmin, xmax, n)[ix]
        imag_part = np.linspace(ymin, ymax, m)[iy] * complex(0, 1)

        c = real_part + imag_part

        return c

    @abstractmethod
    def generate(self, n, m, xmin, xmax, ymin, ymax, itermax):
        """
        Generates a fractal.
        :param n: Pixel resolution in x-axis
        :param m: Pixel resolution in y-axis
        :param itermax: Maximum number of iterations permitted in each calculation
        :param xmin: Minimum x-coord (real number line)
        :param xmax: Maximum x-coord (real number line)
        :param ymin: Minimum y-coord (imag number line)
        :param ymax: Maximum y-coord (imag number line)
        :return: Image representation of the fractal
        :rtype: numpy.lib.twodim_base
        """
        return None

    def display(self):
        fractal = self.generate(500, 500, -1, .5, -1.25, 0.75, 100)
        pylab.imshow(fractal, origin='lower left')
        pylab.show()


class FractalMandel(Fractal):

    def __init__(self):
        Fractal.__init__(self)
        self.name = "Mandelbrot Set"

    def generate(self, n, m, xmin, xmax, ymin, ymax, itermax):

        c = self.get_complex_plane(n, m, xmin, xmax, ymin, ymax)

        # Generates a fresh matrix with the same dimensions of c which will represent our image
        img = np.matlib.zeros(c.shape, dtype=int)

        # Copy the seed values c into z - this is the matrix which we will actually manipulate
        z = np.copy(c)

        for i in xrange(itermax):  # Like range, except it creates values to iterate through as needed rather than list
            # Mandelbrot function is: f(z) = z^2 + c
            z *= z
            z += c

            # If a value exceeds 2.0, it is bound to approach infinity
            # Get a matrix of all values which are unbounded
            unbounded = abs(z) > 2.0

            # Get all values which are unbounded, and write to them the number of iterations before they became unbounded
            img[unbounded] = i + 1

        # Returns transpose of the image matrix
        return img.T

class FractalJulia(Fractal):

    def __init__(self):
        Fractal.__init__(self)
        self.name = "Julia Set"

        self.seed = complex(0, 0.64)

    def generate(self, n, m, xmin, xmax, ymin, ymax, itermax):

        z = self.get_complex_plane(n, m, xmin, xmax, ymin, ymax)

        # Generates a fresh matrix with the same dimensions of c which will represent our image
        img = np.matlib.zeros(z.shape, dtype=int)

        c = self.seed

        for i in xrange(itermax):
            z *= z
            z += c

            # If a value exceeds 2.0, it is bound to approach infinity, so get a matrix of unbounded points
            unbounded = abs(z) > 2.0

            # Get all values which are unbounded, and write to them the number of iterations before they became unbounded
            img[unbounded] = i + 1

        # Returns transpose of the image matrix
        return img.T

class FractalNewton(Fractal):

    def __init__(self):
        Fractal.__init__(self)
        self.name = "Newton fractal"

        self.seed = complex(0, 0.64)

    @staticmethod
    def f(x):
        """Seed function of which this will be approximating the root"""
        return np.power(x, 3) + 1

    @staticmethod
    def dx(x):
        """Derivative of the seed function"""
        return 3 * np.power(x, 2)

    @staticmethod
    def newtons_iter(f, dx, x):
        """Approximates the root of the inputted function using one iteration of Newton's method"""
        return x - (f(x) / dx(x))

    def generate(self, n, m, xmin, xmax, ymin, ymax, itermax):

        z = self.get_complex_plane(n, m, xmin, xmax, ymin, ymax)

        # Identifies which starting points approach a solution in fewer iterations
        root_iters = np.matlib.zeros(z.shape)

        # When an approximation comes within this of the root, mark the approximation as a solution
        e = 0.00000001

        for i in xrange(itermax):
            z = self.newtons_iter(self.f, self.dx, z)

            # Increment the points in the roots_iters matrix where solutions have been found
            roots = np.where(abs(self.f(z)) < e)
            np.add.at(root_iters, roots, 1.0)

        # Convert the matrix of complex roots into a matrix which can be represented as an image
        roots = z.real + z.imag
        img = (25 * roots + 1 * root_iters).astype(dtype=int)

        # Returns transpose of the image matrix
        return img.T