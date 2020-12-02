import enum
from shimekiri import Logger
from PySide2 import QtCore
from PySide2 import QtWidgets
from shimekiri import fileFn


@enum.unique
class DisplayEnum(enum.Enum):
    days = 0
    hours = 1
    minutes = 2
    seconds = 3


class IntervalEnum(enum.Enum):
    hour = 3600000
    minute = 60000
    second = 1000


class Deadline:
    def __init__(self, name: str, datetime: QtCore.QDateTime, notes: str = ""):
        """
        docstring
        """
        self.name = name
        self.until = datetime
        self.notes = notes
        self.timeformat = "hh:mm:ss"

    def get_days_remaining(self):
        return QtCore.QDateTime.currentDateTime().daysTo(self.until)

    def get_hours_remaining(self):
        return QtCore.QDateTime.currentDateTime().secsTo(self.until) // 3600

    def get_seconds_remaining(self):
        return QtCore.QDateTime.currentDateTime().secsTo(self.until)

    def get_minutes_remaining(self):
        return QtCore.QDateTime.currentDateTime().secsTo(self.until) // 60

    def as_dict(self):
        dl_dict = {"until": self.until.toString(),
                   "notes": self.notes,
                   "timeformat": self.timeformat}
        return dl_dict


class DeadlineWidget(QtWidgets.QWidget):

    DEADLINE_FILE = fileFn.get_data_dir() / "shimekiri" / "deadlines.json"

    def __init__(self,
                 deadline: Deadline,
                 parent=None,
                 style="",
                 display=DisplayEnum.seconds,
                 interval_type=IntervalEnum.second,
                 interval_mult: int = 1):

        super().__init__(parent)
        self.deadline = deadline
        self.style = style
        self.display = display
        self.interval_mult = interval_mult
        self.interval_type = interval_type
        self.interval = self.interval_type.value * interval_mult
        self.timer = QtCore.QTimer(self)

        self.setStyleSheet(self.style)
        self.setToolTip(self.deadline.notes)

        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.start_countdown()

    def create_actions(self):
        pass

    def create_widgets(self):
        self.name_label = QtWidgets.QLabel(self.deadline.name)
        self.until_label = QtWidgets.QLabel()

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.until_label)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.timer.timeout.connect(self.update_time)

    def start_countdown(self):
        self.timer.start(self.interval)

    def update_time(self):
        if self.display.value == DisplayEnum.days.value:
            self.until_label.setText(f"{self.deadline.get_days_remaining()} days left")
        elif self.display.value == DisplayEnum.hours.value:
            self.until_label.setText(f"{int(self.deadline.get_hours_remaining())} hours left")
        elif self.display.value == DisplayEnum.minutes.value:
            self.until_label.setText(f"{int(self.deadline.get_minutes_remaining())} minutes left")
        elif self.display.value == DisplayEnum.seconds.value:
            self.until_label.setText(f"{self.deadline.get_seconds_remaining()} seconds left")

    def as_dict(self) -> dict:
        dl_dict = self.deadline.as_dict()
        dl_dict["display"] = self.display.name
        dl_dict["style"] = self.style
        dl_dict["update_interval"] = self.interval_type.name
        dl_dict["update_mult"] = self.interval_mult
        return dl_dict
