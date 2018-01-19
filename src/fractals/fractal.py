import matplotlib as mpl
import numpy as np
import time

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap

from controls import ControlsInterface
import utils


class Fractal(QObject):

    # Custom signals.
    renderRequested = pyqtSignal()
    renderFinished = pyqtSignal(QPixmap)

    # Static constants.
    FRACTALS = []
    _ID = 0

    def __init__(self, name):
        super(Fractal, self).__init__()

        self._id = Fractal._ID
        self.name = name

        # Initialize default values.
        self.resetZoom()
        self.xres = 300
        self.yres = 300
        self.itermax = 50
        self.colors = 5
        self.colorOffset = 0

        # Create UI.
        self.controls = ControlsInterface()
        self.controls.valueChanged.connect(self._valueChanged)
        self._createControls()

        # Keep static reference to this Fractal instance.
        Fractal.FRACTALS.append(self)
        Fractal._ID += 1

    def render(self):
        """Create RGB image representing fractal."""        
        complex_plane = self._complexPlane(
            self.xres, self.yres, self.xmin, self.ymin, self.xmax, self.ymax)
        kwargs = self.controls.args()
        fractal = self._computeFractal(complex_plane, self.itermax, **kwargs)
        rgb_image = self._toRgbImage(fractal, self.colors, self.colorOffset)
        rgb_image = np.ascontiguousarray(rgb_image)

        # Convert RGB image (numpy array) to QPixmap.
        height, width, channel = rgb_image.shape
        bytesPerLine = 3 * width
        image = QImage(rgb_image.data, 
            width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        # Update listeners.
        self.renderFinished.emit(pixmap)

    def _toRgbImage(self, fractal, colors, color_offset):
        """
        Convert the generated fractal into an RGB image array.

        :param colors: Number of colors permitted in image
        :param color_offset: Default offset for generating color hues
        :return: ndarry of shape (n, m, 3)
        """
        fractal_color_adjusted = utils.adjustRange(fractal)
        rgb_image = np.array([
            fractal_color_adjusted, 
            np.zeros(fractal.shape), 
            np.zeros(fractal.shape)]
        ).astype(dtype=np.uint8)

        return rgb_image.T

    def _complexPlane(self, n, m, xmin, ymin, xmax, ymax):
        """Return matrix representing the complex plane."""
        # Create two matrices of size n x m,
        # [0, 1 ...   and [0, 0 ...
        #  0, 1 ...]       1, 1 ...]
        ix, iy = np.mgrid[0:n, 0:m]

        # Create range of values in the x- and y-axis
        real_part = np.linspace(xmin, xmax, n)[ix]
        imag_part = np.linspace(ymin, ymax, m)[iy] * complex(0, 1)

        complex_plane = real_part + imag_part
        return complex_plane

    def resetZoom(self):
        """Set zoom to original default values."""
        self.xmin, self.ymin, self.xmax, self.ymax = self.defaultZoom()

    def zoom(self, factor):
        """Zoom into fractal by given factor."""
        image_width = self.xmax - self.xmin
        image_height = self.ymax - self.ymin
        zoom_x = factor * image_width
        zoom_y = factor * image_height
        self.xmin += zoom_x / 2
        self.xmax -= zoom_x / 2
        self.ymin += zoom_y / 2
        self.ymax -= zoom_y / 2

        self.renderRequested.emit()

    def _computeFractal(self, complex_plane, **kwargs):
        """Return matrix representing computed fractal."""
        raise NotImplementedError

    def _createControls(self):
        """Create UI for editing fractal generation parameters."""
        return

    def resetControls(self):
        """Reset UI to its default state."""
        # TODO
        return

    def defaultZoom(self):
        """Return tuple, (xmin, ymin, xmax, ymax), representing default 
           zoom level for this fractal."""
        return [-1.0, -1.0, 1.0, 1.0]

    def _valueChanged(self):
        """Called upon any fractal control being modified."""
        self.renderRequested.emit()
