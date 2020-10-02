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


class IntervalWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, label_text="", spinbox_value=1, combobox_options=[]):
        super().__init__(parent)
        self.label = QtWidgets.QLabel(label_text)
        if not label_text:
            self.label.hide()
        self.mult_spinbox = QtWidgets.QSpinBox()
        self.mult_spinbox.setMinimum(1)
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(combobox_options)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.mult_spinbox)
        self.main_layout.addWidget(self.combobox)
        self.setLayout(self.main_layout)


class DeadlineListWidget(QtWidgets.QListWidget):
    itemsReordered = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.installEventFilter(self)

        self.edit_action = QtWidgets.QAction("Edit")
        self.delete_action = QtWidgets.QAction("Delete")
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def eventFilter(self, sender, event):
        if event.type() == QtCore.QEvent.ChildRemoved:
            self.itemsReordered.emit()
        return False

    def show_context_menu(self, point):
        context_menu = QtWidgets.QMenu()
        context_menu.addAction(self.edit_action)
        context_menu.addAction(self.delete_action)
        context_menu.exec_(self.mapToGlobal(point))
