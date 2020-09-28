from datetime import datetime
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from shimekiri import Logger
from shimekiri import Config
from shimekiri.deadline import Deadline
from shimekiri import directories


class WatcherDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Tool)

        # Setup UI
        self.setWindowTitle("Shimekiri")
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint)
        self.setMinimumSize(200, 300)

        # Create widgets
        watcher = WatcherWidget()
        self.setCentralWidget(watcher)


class WatcherWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.setContentsMargins(0, 0, 0, 0)

    def create_actions(self):
        pass

    def create_widgets(self):
        self.deadline_list = QtWidgets.QListWidget()
        self.add_button = QtWidgets.QPushButton("+")

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.deadline_list)
        self.main_layout.addWidget(self.add_button)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.add_button.clicked.connect(self.create_new_deadline)

    def create_new_deadline(self) -> Deadline:
        testdl = Deadline("test", datetime(2020, 12, 13))
        self.add_deadline(testdl)

    def add_deadline(self, deadline: Deadline):
        list_item = QtWidgets.QListWidgetItem()
        deadline_wgt = DeadlineWidget(deadline)
        self.deadline_list.addItem(list_item)
        self.deadline_list.setItemWidget(list_item, deadline_wgt)
        list_item.setSizeHint(deadline_wgt.size())


class DeadlineWidget(QtWidgets.QWidget):
    def __init__(self, deadline: Deadline, parent=None):
        super().__init__(parent)
        self.deadline = deadline
        Logger.debug(deadline.name)

        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_actions(self):
        pass

    def create_widgets(self):
        self.name_label = QtWidgets.QLabel(self.deadline.name)
        self.date_label = QtWidgets.QLabel(self.deadline.until.strftime(Config.get("dateformat") + " " + Config.get("timeformat")))

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.date_label)
        self.setLayout(self.main_layout)

    def create_connections(self):
        pass
