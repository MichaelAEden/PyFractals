from abc import abstractmethod, ABCMeta

import numpy as np
import numpy.matlib
import time

import pylab # TODO: remove with pip

from PIL import Image

class Fractal(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = None
        self.fractal_map = None

    def generate_fractal(self, n, m, xmin, xmax, ymin, ymax, itermax, seeds):
        start = time.clock()
        self.fractal_map = self.generate(n, m, xmin, xmax, ymin, ymax, itermax, seeds)
        stop = time.clock()

        elapsed_time = stop - start

        print "Time elapsed: " + str(elapsed_time)

    @abstractmethod
    def generate(self, n, m, xmin, xmax, ymin, ymax, itermax, seeds):
        """
        Generates a fractal.
        :param n: Pixel resolution in x-axis
        :param m: Pixel resolution in y-axis
        :param itermax: Maximum number of iterations permitted in each calculation
        :param xmin: Minimum x-coord (real number line)
        :param xmax: Maximum x-coord (real number line)
        :param ymin: Minimum y-coord (imag number line)
        :param ymax: Maximum y-coord (imag number line)
        :param seed: Seed for the fractal (unique to each kind of fractal)
        :return: Image representation of the fractal
        :rtype: numpy.lib.twodim_base
        """
        return None

    def get_image_array(self):
        fractal_map = self.fractal_map
        if fractal_map is None:
            raise Exception("Fractal not generated!")

        color_adjusted_fractal_map = self.adjust_color(fractal_map, (0, 255))
        zeroes_map = np.zeros(fractal_map.shape)

        # Layers the three arrays into one 3d image
        data = np.array([color_adjusted_fractal_map, zeroes_map, zeroes_map]).astype(dtype=np.uint8)
        return data.T

    def display(self):
        img = Image.fromarray(self.get_image_array(), 'RGB')
        img.save('temp.png')
        img.show()

    @staticmethod
    def adjust_color(image, color_range):
        """
        Adjusts color of image so the maximum and minimum values in the array match those in the given color range
        :param image: Image array
        :type image: np.ndarray
        :param color_range: Minimum and maximum color range values
        :type color_range: tuple
        :return: Image array adjusted for color
        """

        color_min = color_range[0]
        color_range = color_range[1] - color_min

        max_value = np.nanmax(image)

        color_adjusted_image = (image.astype(dtype=float) / max_value * color_range + color_min).astype(dtype=np.uint8)
        return color_adjusted_image

    def get_complex_plane(self, n, m, xmin, xmax, ymin, ymax):
        """Returns a matrix representing the complex plane."""

        # Creates two matrices of size n x m
        ix, iy = np.mgrid[0:n, 0:m]

        # Here we create a range of values in the x- and y-axis, then multiply by the matrices created before
        real_part = np.linspace(xmin, xmax, n)[ix]
        imag_part = np.linspace(ymin, ymax, m)[iy] * complex(0, 1)

        c = real_part + imag_part

        return c

class FractalMandel(Fractal):
    def __init__(self):
        Fractal.__init__(self)
        self.name = "Mandelbrot Set"

    def generate(self, n, m, xmin, xmax, ymin, ymax, itermax, seed):
        c = self.get_complex_plane(n, m, xmin, xmax, ymin, ymax)
        z = np.copy(c)

        # Generates a fresh matrix with the same dimensions of c which will represent our image
        img = np.matlib.zeros(c.shape, dtype=int)

        for i in xrange(itermax):  # Like range, except it creates values to iterate through as needed rather than list
            # Mandelbrot function is: f(z) = z^2 + c
            z = np.power(z, 2)
            z += c

            # If a value exceeds 2.0, it is bound to approach infinity
            # Get a matrix of all values which are unbounded
            unbounded = abs(z) > 2.0

            # Get all values which are unbounded, and write to them the number of iterations before they became unbounded
            img[unbounded] = i + 1

        # Returns the image matrix
        return img


class FractalJulia(Fractal):
    def __init__(self):
        Fractal.__init__(self)
        self.name = "Julia Set"

    def generate(self, n, m, xmin, xmax, ymin, ymax, itermax, seed):
        c = seed
        z = self.get_complex_plane(n, m, xmin, xmax, ymin, ymax)

        # Generates a fresh matrix with the same dimensions of c which will represent our image
        img = np.matlib.zeros(z.shape, dtype=int)

        for i in xrange(itermax):
            z *= z
            z += c

            # If a value exceeds 2.0, it is bound to approach infinity, so get a matrix of unbounded points
            unbounded = abs(z) > 2.0

            # Get all values which are unbounded, and write to them the number of iterations before they became unbounded
            img[unbounded] = i + 1

        # Returns the image matrix
        return img


class FractalNewton(Fractal):
    def __init__(self):
        Fractal.__init__(self)
        self.name = "Newton fractal"

    @staticmethod
    def newtons_iter(f, dx, x, a=1):
        """Approximates the root of the inputted function using one iteration of Newton's method"""
        return x - a * (f(x) / dx(x))

    def generate(self, n, m, xmin, xmax, ymin, ymax, itermax, seeds):
        f = seeds['f']
        dx = seeds['dx']
        a = seeds['a']
        z = self.get_complex_plane(n, m, xmin, xmax, ymin, ymax)

        # Tracks the number of iterations required to reach a solution
        root_iters = np.matlib.zeros(z.shape)

        # When an approximation comes within this of the root, mark the approximation as a solution
        e = 0.00000001

        for i in xrange(itermax):
            z = self.newtons_iter(f, dx, z, a)

            # Increment the points in the roots_iters matrix where solutions have been found
            roots = np.where(abs(f(z)) < e)
            np.add.at(root_iters, roots, 1.0)

        solutions = z

        # Returns the image matrix
        return [solutions.real, solutions.imag, root_iters]

    def get_image_array(self):
        fractal_map = self.fractal_map
        if fractal_map is None:
            raise Exception("Fractal not generated!")

        color_adjusted_real_map = self.adjust_color(fractal_map[0], (0, 128))
        color_adjusted_imag_map = self.adjust_color(fractal_map[1], (64, 128))
        color_adjusted_iter_map = self.adjust_color(fractal_map[2], (128, 255))

        # Layers the three arrays into one 3d image
        data = np.array([color_adjusted_real_map,
                         color_adjusted_imag_map,
                         color_adjusted_iter_map]).astype(dtype=np.uint8)
        return data.T
