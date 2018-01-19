import matplotlib as mpl
import numpy as np
import numpy.matlib

from controls import ValueControl
from fractal import Fractal


class Julia(Fractal):

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
                (fractal + color_offset) * colors % 1,

                # Saturation = fractal value.
                fractal,

                # Value = 1.
                np.ones(fractal.shape)
            ]
        ).astype(dtype=float).T      

        rgb_img = (mpl.colors.hsv_to_rgb(hsv_img) * 255).astype(dtype=np.uint8)
        return rgb_img

    def _computeFractal(self, complex_plane, itermax, cr=1.0, ci=0.0):
        c = complex(cr, ci)
        z = complex_plane

        # Create matrix to represent this fractal.
        fractal = np.matlib.zeros(z.shape, dtype=float)

        for i in xrange(itermax):
            z = np.square(z) + c

            # Fractal shows number of iterations before values 'escape'
            np.copyto(
                fractal,
                fractal + np.exp(-np.absolute(z)),
                casting='no',
                where=np.invert(np.isnan(z))
            )

        # Represent fractal as floats ranging between 0 and 1.
        fractal /= itermax
        fractal[fractal > 1] = 1
        fractal[fractal < 0] = 0

        # Returns the image matrix
        return fractal

    def _createControls(self):
        """Create UI for editing fractal generation parameters."""
        c_control = ValueControl("cr", vmin=-2, vmax=3, default=2, precision=2)
        i_control = ValueControl("ci", vmin=-2, vmax=3, default=2, precision=2)
        self.controls.addControl("Real Value", c_control)
        self.controls.addControl("Real Value", i_control)