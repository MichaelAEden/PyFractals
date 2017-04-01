from abc import abstractmethod, ABCMeta

import numpy as np
import numpy.matlib

import pylab

class Fractal(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = None

    @abstractmethod
    def generate(self, n, m, itermax, xmin, xmax, ymin, ymax):
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
        fractal = self.generate(1000, 1000, 200, -1, 1, -1, 1)
        pylab.imshow(fractal, origin='lower left')
        pylab.show()


class FractalMandel(Fractal):

    def __init__(self):
        Fractal.__init__(self)
        self.name = "Mandelbrot Set"

    def generate(self, n, m, itermax, xmin, xmax, ymin, ymax):
        # Creates two matrices of size n x m, m x n
        ix, iy = np.mgrid[0:n, 0:m]

        # NOTE: linspace is essentially the same as range, but it returns a numpy.ndarray object
        # Here we create a range of values in the x- and y-axis, then multiply these values by the matrices we
        # generated before
        real_part = np.linspace(xmin, xmax, n)[ix]
        imag_part = np.linspace(ymin, ymax, m)[iy] * complex(0, 1)

        # Now generate a matrix representing the complex plane from from xmin - xmax, ymin - ymax
        c = real_part + imag_part

        # These are no longer needed so we can delete these
        del real_part, imag_part

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
            img[ix[unbounded], iy[unbounded]] = i + 1

        # Returns transpose of the image matrix
        return img.T

class FractalJulia(Fractal):

    def __init__(self):
        Fractal.__init__(self)
        self.name = "Julia Set"

        self.seed = complex(0, 0.64)

    def generate(self, n, m, itermax, xmin, xmax, ymin, ymax):
        # Creates two matrices of size n x m, m x n
        ix, iy = np.mgrid[0:n, 0:m]

        # NOTE: linspace is essentially the same as range, but it returns a numpy.ndarray object
        # Here we create a range of values in the x- and y-axis, then multiply these values by the matrices we
        # generated before
        real_part = np.linspace(xmin, xmax, n)[ix]
        imag_part = np.linspace(ymin, ymax, m)[iy] * complex(0, 1)

        # Now generate a matrix representing the complex plane from from xmin - xmax, ymin - ymax
        z = real_part + imag_part

        # These are no longer needed so we can delete these
        del real_part, imag_part

        # Generates a fresh matrix with the same dimensions of c which will represent our image
        img = np.matlib.zeros(z.shape, dtype=int)

        # Copy the seed values c into z - this is the matrix which we will actually manipulate
        c = self.seed

        for i in xrange(itermax):  # Like range, except it creates values to iterate through as needed rather than list
            # Mandelbrot function is: f(z) = z^2 + c
            z *= z
            z += c

            # If a value exceeds 2.0, it is bound to approach infinity
            # Get a matrix of all values which are unbounded
            unbounded = abs(z) > 2.0

            # Get all values which are unbounded, and write to them the number of iterations before they became unbounded
            img[ix[unbounded], iy[unbounded]] = i + 1

        # Returns transpose of the image matrix
        return img.T