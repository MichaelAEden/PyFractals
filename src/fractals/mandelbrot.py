import matplotlib as mpl
import numpy as np
import numpy.matlib

from controls import ValueControl
from fractal import Fractal


class Mandelbrot(Fractal):

    def _computeFractal(self, complex_plane, itermax, p=2):
        c = complex_plane
        z = np.copy(c)

        # Create matrix to represent this fractal and escaped values.
        fractal = np.matlib.zeros(c.shape, dtype=float)
        escaped = np.matlib.zeros(c.shape, dtype=bool)

        for i in xrange(itermax):
            # Mandelbrot function is: f(z) = z^p + c; p is const.
            if p == 2.0:
                z = np.square(z)  # Runs much faster than np.power(z, 2).
            else:
                z = np.power(z, p)
            z += c

            # Smooth borders in fractal.
            temp_escaped = (abs(z) > 2.0)
            np.copyto(
                fractal,
                (i + 1 - np.log(np.log(np.absolute(z))) / np.log(2)),
                casting='no',
                where=np.invert(escaped) & temp_escaped
            )
            escaped = temp_escaped

        # Represent fractal as floats ranging between 0 and 1.
        fractal /= itermax
        fractal[fractal > 1] = 1
        fractal[fractal < 0] = 0

        return fractal

    def _toRgbImage(self, fractal, colors, color_offset):
        """
        Convert the generated fractal into an RGB image array.

        :param colors: Number of colors permitted in image
        :param color_offset: Default offset for generating color hues
        :return: ndarry of shape (n, m, 3)
        """
        colour_count = 5
        hsv_img = np.array(
            [
                # Cycle through color wheel.
                (fractal + color_offset) * colour_count % 1,

                # Saturation = 1 where fractal values > 0,
                # Saturation = 0 otherwise.
                fractal.astype(dtype=bool).astype(dtype=float),

                # Invert colours
                1 - fractal
            ]
        ).astype(dtype=float).T

        rgb_img = (mpl.colors.hsv_to_rgb(hsv_img) * 255).astype(dtype=np.uint8)
        return rgb_img

    def _createControls(self):
        """Create UI for editing fractal generation parameters."""
        p_control = ValueControl("p", vmin=-2, vmax=3, default=2, precision=2)
        self.controls.addControl("Power", p_control)
