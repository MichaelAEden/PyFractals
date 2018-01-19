from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSlider
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit


class ControlsInterface(QWidget):

    # Custom signals.
    valueChanged = pyqtSignal()

    def __init__(self):
        super(ControlsInterface, self).__init__()

        self._controls = []

        # Create main layout.
        self._formLayout = QFormLayout()
        self.setLayout(self._formLayout)

    def addControl(self, label, control):
        control.valueChanged.connect(self._valueChanged)
        self._controls.append(control)
        self._formLayout.addRow(QLabel(label), control)

    def args(self):
        """Return dictionary of user inputted-values."""
        args = {}
        for control in self._controls:
            args[control.key()] = control.value()
        return args

    def _valueChanged(self):
        self.valueChanged.emit()


class Control(QWidget):
    """Custom widget for modifying value."""

    # Custom signals.
    valueChanged = pyqtSignal()

    def __init__(self, key, default):
        super(Control, self).__init__()
        self._key = key
        self._default = default
        self._value = default

    def reset(self):
        self.setValue(self._default)

    def setValue(self, value):
        return

    def key(self):
        return self._key

    def value(self):
        return self._value


class OptionSelect(Control):
    """Custom widget for selecting from a list of options."""

    def __init__(self, key, default, options):
        super(OptionSelect, self).__init__(key, default)

        self._default = default
        self._options = options

        # Create controls.
        self._selector = QComboBox()
        self._selector.setMinimumWidth(500)
        self._selector.currentIndexChanged.connect(self._optionSelected)
        for option in options:
            self._selector.addItem(option.name)

        # Create layout.
        layout = QHBoxLayout()
        layout.addWidget(self._selector)
        self.setLayout(layout)

        # Reset to default state.
        self.reset()

    def setValue(self, value):
        index = self._options.index(value)
        self._selector.setCurrentIndex(index)

    def _optionSelected(self, index):
        self._value = self._options[index]
        self.valueChanged.emit()


class ValueControl(Control):
    """Custom widget for modifying a float value."""

    def __init__(self, key, default, vmin, vmax, precision=5):
        super(ValueControl, self).__init__(key, default)

        self._default = default
        self._min = vmin
        self._max = vmax
        self._precision = precision

        # Create controls.
        self._valueField = QLineEdit()
        self._valueField.setMinimumWidth(100)
        self._valueField.editingFinished.connect(self._valueEntered)
        self._valueSlider = FloatSlider(vmin, vmax, precision)
        self._valueSlider.setMinimumWidth(500)
        self._valueSlider.valueFChanged.connect(self._valueChanged)

        # Create layout.
        layout = QHBoxLayout()
        layout.addWidget(self._valueField)
        layout.addWidget(self._valueSlider)
        self.setLayout(layout)

        # Reset to default state.
        self.reset()

    def setValue(self, value):
        self._valueSlider.setValueF(value)
        self._valueField.setText(str(value))

    def _valueEntered(self):
        """Called upon value typed into field."""
        try:
            value = float(self._valueField.text())
            value = round(value, self._precision)
            valid_input = (self._min < value < self._max)
        except ValueError:
            # User entered non-numerical value.
            valid_input = False

        if not valid_input:
            # Reset value to last valid input.
            self._valueField.setText(str(self._value))
            return

        self._value = value
        self._valueSlider.setValueF(value)

        # Update listeners.
        self.valueChanged.emit()

    def _valueChanged(self, value):
        """Called upon slider moved."""
        self._valueField.setText(str(value))
        self._value = value
        self.valueChanged.emit()


class FloatSlider(QSlider):
    """Custom slider with float values of custom precision."""

    valueFChanged = pyqtSignal(float)

    def __init__(self, vmin, vmax, precision):
        super(FloatSlider, self).__init__(Qt.Horizontal)

        self._precision = precision

        self.setMinimum(vmin * 10 ** precision)
        self.setMaximum(vmax * 10 ** precision)
        self.setTickPosition(QSlider.NoTicks)
        self.setSingleStep(1)
        self.sliderMoved.connect(self._valueChanged)

    def setValueF(self, value):
        self.setValue(value * 10 ** self._precision)

    def _valueChanged(self, value):
        self.valueFChanged.emit(value / 10.0 ** self._precision)
