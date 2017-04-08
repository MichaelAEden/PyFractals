from abc import abstractmethod, ABCMeta

import numpy as np
import numpy.matlib
import time

import matplotlib as mpl
import rendercolor


class Fractal(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = None
        self.fractal_map = None

    def get_fractal_image(self, n, m, itermax, xmin, xmax, ymin, ymax, *args, **kwargs):
        start = time.clock()
        fractal_map = self.generate_fractal(n, m, itermax, xmin, xmax, ymin, ymax, *args, **kwargs)
        stop = time.clock()

        elapsed_time = stop - start
        print "Time elapsed: " + str(elapsed_time)

        rgb_image = self.fractal_to_rgb_image(fractal_map)

        return rgb_image

    @abstractmethod
    def generate_fractal(self, n, m, itermax, xmin, xmax, ymin, ymax, *args, **kwargs):
        """
        Generates a fractal as a numpy array.
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

    def fractal_to_rgb_image(self, fractal_map):
        """
        Converts the generated fractal into an RGB image array
        :return: ndarry of shape (n, m, 3)
        """
        color_adjusted_fractal_map = rendercolor.adjust_color(fractal_map, (0, 255))
        zeroes_map = np.zeros(fractal_map.shape)

        # Layers the three arrays into one 3d image
        data = np.array([color_adjusted_fractal_map, zeroes_map, zeroes_map]).astype(dtype=np.uint8)
        return data.T

    @staticmethod
    def get_complex_plane(n, m, xmin, xmax, ymin, ymax):
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
        self.num_colors = -1

    def fractal_to_rgb_image(self, fractal_map):
        hsv_img = np.array(
            [fractal_map * self.num_colors % 1,  # Cycles through the color wheel
             fractal_map.astype(dtype=bool).astype(dtype=float),  # Sets saturation to either 0 at zero points
             # or 1 at any non-zero points
             1 - fractal_map]).astype(dtype=float).T  # Values become darker

        rgb_img = (mpl.colors.hsv_to_rgb(hsv_img) * 255).astype(dtype=np.uint8)
        return rgb_img

    def generate_fractal(self, n, m, itermax, xmin, xmax, ymin, ymax, num_colors, p):
        self.num_colors = num_colors

        p = p
        c = self.get_complex_plane(n, m, xmin, xmax, ymin, ymax)
        z = np.copy(c)

        # Generates a matrix with the same dimensions of c which will represent our image
        smooth_img = np.matlib.zeros(c.shape, dtype=float)
        escaped = np.matlib.zeros(c.shape, dtype=bool)

        for i in xrange(itermax):  # Like range, except it creates values to iterate through as needed rather than list

            # Mandelbrot function is: f(z) = z^2 + c, but we can also sub 2 for other values
            if p == 2.0:
                z = np.square(z)  # Runs much faster than np.power(z, 2), so we have a special case
            else:
                z = np.power(z, p)

            z += c

            # In the image, use the current iteration minus some calculated value to get the final smoothed colour
            temp_escaped = (abs(z) > 2.0)
            np.copyto(
                smooth_img,
                (i + 1 - np.log(np.log(np.absolute(z))) / np.log(2)),
                casting='no',
                where=np.invert(escaped) & temp_escaped
            )
            escaped = temp_escaped

        # Smooth colours are ranged (0, itermax), so we must put them in range (0, 1)
        smooth_img /= itermax
        smooth_img[smooth_img > 1] = 1
        smooth_img[smooth_img < 0] = 0

        # Returns the image matrix
        return smooth_img


class FractalPheonix(Fractal):
    def __init__(self):
        Fractal.__init__(self)
        self.name = "Pheonix Fractal"

    def generate_fractal(self, n, m, itermax, xmin, xmax, ymin, ymax, seed):
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

    def fractal_to_rgb_image(self, fractal_map):
        fractal_map = self.fractal_map
        hsv_img = np.array(
            [(fractal_map + 0.05) * self.num_colors % 1,
             fractal_map,
             np.ones(fractal_map.shape)]).astype(dtype=float).T

        rgb_img = (mpl.colors.hsv_to_rgb(hsv_img) * 255).astype(dtype=np.uint8)
        return rgb_img

    def generate_fractal(self, n, m, itermax, xmin, xmax, ymin, ymax, seed):
        self.num_colors = seed['num_colors']
        c = seed['c']
        z = self.get_complex_plane(n, m, xmin, xmax, ymin, ymax)

        # Generates a fresh matrix with the same dimensions of c which will represent our image
        smooth_img = np.matlib.zeros(z.shape, dtype=float)

        for i in xrange(itermax):
            z = np.square(z) + c

            # Get all values which are unbounded, and write to them the number of iterations before they became unbounded
            np.copyto(
                smooth_img,
                smooth_img + np.exp(-np.absolute(z)),
                casting='no',
                where=np.invert(np.isnan(z))
            )

        # Smooth colours are ranged (0, itermax), so we must put them in range (0, 1)
        smooth_img /= itermax
        smooth_img[smooth_img > 1] = 1
        smooth_img[smooth_img < 0] = 0

        # Returns the image matrix
        return smooth_img


class FractalNewton(Fractal):
    @staticmethod
    def f_sin(x):
        return np.sin(x)

    @staticmethod
    def dx_sin(x):
        return np.cos(x)

    @staticmethod
    def f_trig_composite(x):
        return np.cos(np.sin(x)) - np.pi

    @staticmethod
    def dx_trig_composite(x):
        return -1 * np.cos(x) * np.sin(np.sin(x))

    @staticmethod
    def f_polynomial(x):
        return np.power(x, 3) + 1

    @staticmethod
    def dx_polynomial(x):
        return 3 * np.power(x, 2)

    FUNCTION_SEED_SIN = (f_sin, dx_sin)
    FUNCTION_SEED_TRIG = (f_sin, dx_sin)
    FUNCTION_SEED_POLYNOMIAL = (f_polynomial, dx_polynomial)

    def __init__(self):
        Fractal.__init__(self)
        self.name = "Newton fractal"

    @staticmethod
    def newtons_iter(f, dx, x, a=1):
        """Approximates the root of the inputted function using one iteration of Newton's method"""
        return x - a * (f(x) / dx(x))

    def generate_fractal(self, n, m, itermax, xmin, xmax, ymin, ymax, seeds):
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

    def fractal_to_rgb_image(self, fractal_map):
        color_adjusted_real_map = rendercolor.adjust_color(fractal_map[0], (0, 64))
        color_adjusted_imag_map = rendercolor.adjust_color(fractal_map[1], (64, 96))
        color_adjusted_iter_map = rendercolor.adjust_color(fractal_map[2], (64, 128))

        # Layers the three arrays into one 3d image
        data = np.array([color_adjusted_real_map,
                         color_adjusted_imag_map,
                         color_adjusted_iter_map]).astype(dtype=np.uint8)

        return data.T
