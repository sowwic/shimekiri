import enum
from logging import setLogRecordFactory
from shimekiri import logger
from PySide2 import QtWidgets
from PySide2 import QtCore
from shimekiri import Logger
from shimekiri import Config
from shimekiri.deadline import Deadline, DeadlineWidget
from shimekiri import directories
from shimekiri import fileFn


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

    DEADLINE_FILE = Config.get_appdata_dir() / "deadlines.json"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.setContentsMargins(0, 0, 0, 0)

        # Load deadline data
        self.update_list()

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
        info_dialog = DeadLineInfoDialog(self)
        result = info_dialog.exec_()
        # if not result == DeadLineInfoDialog.Accepted:
        #     return

        new_dl = Deadline("testy_boi", QtCore.QDateTime(2020, 12, 13, 0, 0, 0))
        data_dict = self.get_deadlines()
        data_dict[new_dl.name] = new_dl.as_dict()
        fileFn.write_json(self.DEADLINE_FILE, data_dict)
        self.update_list()

    def add_deadline_item(self, deadline: Deadline):
        list_item = QtWidgets.QListWidgetItem()
        deadline_wgt = DeadlineWidget(deadline)
        deadline_wgt.update_time()
        self.deadline_list.addItem(list_item)
        self.deadline_list.setItemWidget(list_item, deadline_wgt)
        list_item.setSizeHint(deadline_wgt.size())

    def save_deadlines(self):
        data_dict = self.get_deadlines()

        for item in self.deadline_list.items():
            dl_widget: DeadlineWidget = self.deadline_list.itemWidget(item)
            data_dict[dl_widget.deadline.name] = dl_widget.as_dict()

        fileFn.write_json(self.DEADLINE_FILE, data_dict)
        Logger.debug(f"Saved deadlines: {data_dict}")
        self.update_list()

    def get_deadlines(self) -> dict:
        data_dict = {}
        if self.DEADLINE_FILE.is_file():
            data_dict = fileFn.load_json(self.DEADLINE_FILE)
        else:
            fileFn.create_file(self.DEADLINE_FILE)

        return data_dict

    def import_deadlines(self):
        dl_dict = self.get_deadlines()
        for key in dl_dict:
            dl_instance = Deadline(key, QtCore.QDateTime.fromString(dl_dict[key].get("until", "")), notes=dl_dict[key].get("notes", ""))
            self.add_deadline_item(dl_instance)

    def update_list(self):
        self.deadline_list.clear()
        self.import_deadlines()


class DeadLineInfoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, deadline_obj: Deadline = None):
        super().__init__(parent)

        self.setModal(1)
        self.setMinimumSize(200, 300)
        self.deadline_obj = deadline_obj or Deadline("New deadline", QtCore.QDateTime.currentDateTime())
        Logger.debug(self.deadline_obj.until)

        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_actions(self):
        pass

    def create_widgets(self):
        self.main_widget = QtWidgets.QWidget()

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setLayout(self.main_layout)

    def create_connections(self):
        pass
