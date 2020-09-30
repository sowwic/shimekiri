import enum
from logging import setLogRecordFactory
from PySide2 import QtWidgets
from PySide2 import QtCore
from shimekiri import Logger
from shimekiri import Config
from shimekiri.deadline import Deadline, DeadlineWidget, DisplayEnum, IntervalEnum
from shimekiri import directories
from shimekiri import fileFn
from shimekiri import widgets


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
        if not result == DeadLineInfoDialog.Accepted:
            return

        new_dl, display_options = info_dialog.get_data()
        data_dict = self.get_deadlines()
        data_dict[new_dl.deadline.name] = new_dl.as_dict()
        fileFn.write_json(self.DEADLINE_FILE, data_dict)
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
            deadline_wgt = DeadlineWidget(dl_instance,
                                          style=dl_dict[key].get("style", ""),
                                          display=DisplayEnum[dl_dict[key].get("display", "days")],
                                          interval_type=IntervalEnum[dl_dict[key].get("update_interval", "hour")],
                                          interval_mult=dl_dict[key].get("update_mult", 1))
            deadline_wgt.update_time()

            list_item = QtWidgets.QListWidgetItem()
            self.deadline_list.addItem(list_item)
            self.deadline_list.setItemWidget(list_item, deadline_wgt)
            list_item.setSizeHint(deadline_wgt.size())

    def update_list(self):
        self.deadline_list.clear()
        self.import_deadlines()


class DeadLineInfoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, deadline_widget: DeadlineWidget = None):
        super().__init__(parent)

        self.setModal(1)
        self.setMinimumSize(400, 600)
        self.deadline_widget = deadline_widget or DeadlineWidget(Deadline("New deadline", QtCore.QDateTime.currentDateTime()))

        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_actions(self):
        pass

    def create_widgets(self):
        self.info_grp = QtWidgets.QGroupBox("Info")
        self.display_grp = QtWidgets.QGroupBox("Display")
        self.main_widget = QtWidgets.QWidget()
        self.create_button = QtWidgets.QPushButton("Create")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        # Info
        self.name_lineedit = QtWidgets.QLineEdit(self.deadline_widget.deadline.name)
        self.datetime_edit = QtWidgets.QDateTimeEdit()
        self.datetime_edit.setCalendarPopup(1)
        self.datetime_edit.setAccelerated(1)
        self.datetime_edit.setDateTime(self.deadline_widget.deadline.until)
        self.notes_textedit = QtWidgets.QTextEdit(self.deadline_widget.deadline.notes)

        # Display
        self.countdown_mode = QtWidgets.QComboBox()
        self.countdown_mode.addItems([member.name for member in list(DisplayEnum)])
        self.interval_wgt = widgets.IntervalWidget(label_text="", spinbox_value=1, combobox_options=[member.name for member in list(IntervalEnum)])

    def create_layouts(self):
        self.info_layout = QtWidgets.QFormLayout()
        self.info_layout.addRow("Name:", self.name_lineedit)
        self.info_layout.addRow("Until:", self.datetime_edit)
        self.info_layout.addRow("Notes:", self.notes_textedit)
        self.info_grp.setLayout(self.info_layout)

        self.display_layout = QtWidgets.QFormLayout()
        self.display_layout.addRow("Countdown mode:", self.countdown_mode)
        self.display_layout.addRow("Update interval:", self.interval_wgt)
        self.display_grp.setLayout(self.display_layout)

        self.action_buttons_layout = QtWidgets.QHBoxLayout()
        self.action_buttons_layout.addStretch()
        self.action_buttons_layout.addWidget(self.create_button)
        self.action_buttons_layout.addWidget(self.cancel_button)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.info_grp)
        self.main_layout.addWidget(self.display_grp)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.action_buttons_layout)

        self.main_layout.setContentsMargins(0, 0, 0, 5)
        self.main_widget.setLayout(self.main_layout)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.create_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.close)

    def get_data(self):
        self.deadline_widget.deadline.name = self.name_lineedit.text()
        self.deadline_widget.deadline.until = self.datetime_edit.dateTime()
        self.deadline_widget.deadline.notes = self.notes_textedit.toPlainText()
        self.deadline_widget.display = DisplayEnum[self.countdown_mode.currentText()]
        self.deadline_widget.interval_type = IntervalEnum[self.interval_wgt.combobox.currentText()]
        self.deadline_widget.interval_mult = self.interval_wgt.mult_spinbox.value()

        display_options = {}
        return self.deadline_widget, display_options
