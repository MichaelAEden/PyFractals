import numpy as np
import numpy.matlib

from controls import ValueControl
from fractal import Fractal


class Pheonix(Fractal):

    def _computeFractal(self, complex_plane, itermax, p=2.0, c=1.0):
        z1 = complex_plane
        z0 = np.zeros(complex_plane.shape)

        # Create matrix to represent this fractal.
        fractal = np.matlib.zeros(z1.shape, dtype=int)

        for i in xrange(itermax):
            temp = z1

            # Pheonix function is: zk+1 = zk2 + c + P*zk-1; p, c are const.
            z1 = np.add(np.square(z1), c) + (p * z0)
            z0 = temp

            # Update 'escaped' values in image.
            escaped = (abs(z1) > 2.0)
            fractal[escaped] = i + 1

        return fractal.T
