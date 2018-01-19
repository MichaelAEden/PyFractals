import os
import math
import numpy as np
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QStackedLayout

# QApplication instance.
global app
app = QApplication(sys.argv)

from fractals import fractals


class PyFractal(QWidget):

    # Static constants.
    ZOOM_FACTOR = 0.1
    
    def __init__(self):
        super(PyFractal, self).__init__()
        self._fractal = None

        # Create thread which renders fractals.
        self._fractalThread = QThread()

        # Size and center window.
        self.resize(500, 500)
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.size(),
                app.desktop().availableGeometry()
            )
        )

        self._controlsLabel = QLabel("Controls")
        self._fractalDisplay = FractalDisplay(self)
        self._createZoomControls()
        self._createFractalControls()

        # Create main layout.
        layout = QGridLayout()
        layout.addWidget(self._fractalSelector, 0, 0)
        layout.addWidget(self._fractalDisplay, 1, 0)
        layout.addLayout(self._zoomButtonsLayout, 2, 0)
        layout.addWidget(self._controlsLabel, 0, 1)
        layout.addLayout(self._fractalControls, 1, 1)
        self.setLayout(layout)

        # Reset to default state.
        self._reset()

        self.show()


    def _reset(self):
        """Resets application to default state."""
        # Reset UI.
        self._fractalSelector.setCurrentIndex(0)
        self._fractalSelected(0)
        self._fractal.resetControls()

        # Reset fractal zoom settings.
        self._zoomReset()

        # Update fractal image.
        self._renderRequested()


    # {{{ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # }}} Constructor Helpers

    def _createZoomControls(self):
        """Creates zoom controls for viewing fractals."""
        # Create buttons.
        self._zoomResetButton = QToolButton()
        self._zoomResetButton.setIcon(QIcon.fromTheme("zoom-original"))
        self._zoomResetButton.clicked.connect(self._zoomReset)
        self._zoomInButton = QToolButton()
        self._zoomInButton.setIcon(QIcon.fromTheme("zoom-in"))
        self._zoomInButton.clicked.connect(self._zoomIn)
        self._zoomOutButton = QToolButton()
        self._zoomOutButton.setIcon(QIcon.fromTheme("zoom-out"))
        self._zoomOutButton.clicked.connect(self._zoomOut)

        # Create buttons layout.
        self._zoomButtonsLayout = QHBoxLayout()
        self._zoomButtonsLayout.addWidget(self._zoomResetButton)
        self._zoomButtonsLayout.addWidget(self._zoomInButton)
        self._zoomButtonsLayout.addWidget(self._zoomOutButton)
        self._zoomButtonsLayout.addStretch()

    def _createFractalControls(self):
        """Creates controls for selecting and modifying fractals."""
        self._fractalSelector = QComboBox()
        self._fractalControls = QStackedLayout()
        for fractal in fractals.getFractals():
            self._fractalSelector.addItem(fractal.name)
            self._fractalControls.addWidget(fractal.controls)

        # Connect signals.
        self._fractalSelector.currentIndexChanged.connect(self._fractalSelected)


    # {{{ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # }}} Handlers

    def _zoomReset(self):
        self._fractal.resetZoom()

    def _zoomIn(self):
        self._fractal.zoom(PyFractal.ZOOM_FACTOR)

    def _zoomOut(self):
        self._fractal.zoom(-PyFractal.ZOOM_FACTOR)

    def _renderRequested(self):
        # Create thread for fractal rendering.
        self._fractalThread.quit()
        self._fractalThread.start()

    def _render(self, pixmap):
        self._fractalDisplay.setPixmap(pixmap)

    def _fractalSelected(self, index):
        if self._fractal:
            # Disconnect previous signals.
            self._fractalThread.started.disconnect(self._fractal.render)

        self._fractalControls.setCurrentIndex(index)
        self._fractal = fractals.getFractal(index)
        self._fractal.renderRequested.connect(self._renderRequested)
        self._fractal.renderFinished.connect(self._render)
        self._fractal.moveToThread(self._fractalThread)
        self._fractalThread.started.connect(self._fractal.render)
        self._renderRequested()


class FractalDisplay(QLabel):

    def __init__(self, parent):
        super(FractalDisplay, self).__init__(parent)

        # User input handling.
        self.setMouseTracking(True)
        self._pressed = False


    # {{{ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # }}} Handlers

    def keyPressEvent(self, event):
        # TODO: use arrow keys to navigate.
        super(FractalDisplay, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        self._pressed = True
        super(FractalDisplay, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        super(FractalDisplay, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self._pressed:
            # TODO: move fractal.
            pass

        super(FractalDisplay, self).mouseMoveEvent(event)


if __name__=='__main__':
    # Set options for printing numpy arrays to console.
    np.set_printoptions(threshold=np.nan)
    np.warnings.filterwarnings("ignore")

    # Create main application window.
    window = PyFractal()
    
    # Run application.
    result = app.exec_()
    
    # Remove pyc files.
    pyc_files = (f for f in os.listdir('.') if f.endswith(".pyc"))
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
        except:
            pass

    sys.exit(result)
