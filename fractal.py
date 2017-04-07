from abc import abstractmethod, ABCMeta

import numpy as np
import numpy.matlib
import time
import random

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

    @staticmethod
    def get_weighted_colors(color_1, color_2, color_weight_array):
        if np.nanmax(color_weight_array) > 1.0:
            raise Exception("Color weight cannot be > 1. Invalid color weight: %s" % (str(np.amax(color_weight_array))))

        return color_weight_array * 1
        # return (color_weight_array * float(color_1) + (1.0 + (-1 * color_weight_array)) * float(color_2)).astype(dtype=int)

    def get_image_array(self):
        fractal_map = self.fractal_map[0]
        escape_factors = self.fractal_map[1]

        # print escape_factors

        if fractal_map is None:
            raise Exception("Fractal not generated!")

        # Generates a list of random colors
        color_range = 5     # Number of colors to generate
        colors = [0x000000] # Set black as default color
        for i in range(color_range):
            colors.append(random.randint(1, 0xffffff))
        # print colors

        # Assigns these colors to the fractal based on iterations per pixel
        color_adjusted_fractal_map = fractal_map % color_range
        for color in range(len(colors)):
            # adjust_color_section = color_adjusted_fractal_map[]
            fractal_map[color_adjusted_fractal_map==color] = colors[color]

            # new_colors = escape_factors
            # new_colors = self.get_weighted_colors(colors[color], colors[(color + 1) % len(colors)], escape_factors)

            # print "MAXIMUM: " + str(np.amax(new_colors) / (256 ** 3))

        # TODO: understand bitwise operators
        # Converts the color map into three RGB maps which are then layered on top of each other
        # There may be a much simpler way to do this
        r_map = fractal_map & 255
        g_map = (fractal_map >> 8) & 255
        b_map = (fractal_map >> 16) & 255

        # print r_map
        # print g_map
        # print b_map

        # Layers the three arrays into one 3d image
        data = np.array([r_map, g_map, b_map]).astype(dtype=np.uint8)

        print data.shape

        return data.T

    def generate(self, n, m, xmin, xmax, ymin, ymax, itermax, seed):
        c = self.get_complex_plane(n, m, xmin, xmax, ymin, ymax)
        z = np.copy(c)

        # Generates a matrix with the same dimensions of c which will represent our image
        img = np.matlib.zeros(c.shape, dtype=int)
        escaped = np.matlib.zeros(c.shape, dtype=bool)
        escape_factor = np.matlib.zeros(c.shape, dtype=float)

        for i in xrange(itermax):  # Like range, except it creates values to iterate through as needed rather than list

            # Mandelbrot function is: f(z) = z^2 + c
            z = np.square(z)
            z += c

            # Track which values have escaped and keep track of these iterations in the final image
            temp_escaped = (abs(z) > 2.0)

            # For color smoothing, we keep track of how fast these escaped values
            tracking_points = np.invert(escaped) & temp_escaped
            escape_factor[tracking_points] = np.log(np.absolute(z[tracking_points])) / 2.0

            escaped = temp_escaped
            img[escaped] = i + 1

        # Returns the image matrix
        return [img, escape_factor]


class FractalPheonix(Fractal):
    def __init__(self):
        Fractal.__init__(self)
        self.name = "Pheonix Fractal"

    def generate(self, n, m, xmin, xmax, ymin, ymax, itermax, seed):
        p = seed['P']
        c = seed['c']
        z1 = self.get_complex_plane(n, m, xmin, xmax, ymin, ymax)
        z0 = np.zeros(z1.shape)

        # Generates a matrix with the same dimensions of c which will represent our image
        img = np.matlib.zeros(z1.shape, dtype=int)

        for i in xrange(itermax):  # Like range, except it creates values to iterate through as needed rather than list

            temp = z1

            # Pheonix function is: zk+1 = zk2 + c + P*zk-1
            z1 = np.add(np.square(z1), c) + (p * z0)
            z0 = temp

            # Track which values have escaped and keep track of these iterations in the final image
            escaped = (abs(z1) > 2.0)
            img[escaped] = i + 1

        # Returns the image matrix
        return img.T


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
            z = np.square(z) + c

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
            root_iters[roots] += 1

        solutions = z

        # Returns the image matrix
        return [solutions.real, solutions.imag, root_iters]

    def get_image_array(self):
        fractal_map = self.fractal_map
        if fractal_map is None:
            raise Exception("Fractal not generated!")

        color_adjusted_real_map = self.adjust_color(fractal_map[0], (0, 127))
        color_adjusted_imag_map = self.adjust_color(fractal_map[1], (0, 127))
        color_adjusted_iter_map = self.adjust_color(fractal_map[2], (0, 128))

        # Layers the three arrays into one 3d image
        data = np.array([color_adjusted_real_map + color_adjusted_iter_map,
                         color_adjusted_imag_map + color_adjusted_iter_map,
                         color_adjusted_iter_map]).astype(dtype=np.uint8)
        return data.T
