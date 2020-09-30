from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from shimekiri import Logger


class ColorButton(QtWidgets.QLabel):

    color_changed = QtCore.Signal(QtGui.QColor)

    def __init__(self, parent=None, color=[1, 1, 1]):
        super(ColorButton, self).__init__(parent)

        self._color = QtGui.QColor()  # Invalid color

        self.set_size(25, 25)
        self.set_color(color)

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def set_color(self, color):
        Logger.debug("Set color: {0}".format(color))
        if isinstance(color, list):
            if not color:
                color = [1, 1, 1]
            color = QtGui.QColor.fromRgb(*color)

        color = QtGui.QColor(color)
        if self._color == color:
            return

        self._color = color
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(self._color)
        self.setPixmap(pixmap)
        self.color_changed.emit(self._color)

    def get_color(self):
        return self._color

    def select_color(self):
        color = QtWidgets.QColorDialog.getColor(self.get_color(), self, options=QtWidgets.QColorDialog.DontUseNativeDialog)
        if color.isValid():
            self.set_color(color)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.select_color()
