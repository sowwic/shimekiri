from PySide2 import QtWidgets
from PySide2 import QtCore
from shimekiri import Logger
from shimekiri import Config
from shimekiri.deadline import Deadline


class WatcherDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup UI
        self.setWindowTitle("Shimekiri")
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnBottomHint)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint)
        self.setMinimumSize(200, 300)


class WatcherWidget(QtWidgets.QWidget):
    pass


class DeadlineWidget(QtWidgets.QWidget):
    pass
