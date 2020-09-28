import sys
from PySide2 import QtWidgets
from shimekiri.watcher_ui import WatcherWidget, WatcherDialog
from shimekiri import Logger
from shimekiri import Config
from shimekiri import directories


def load_style(name="diffnes"):
    with open(directories.STYLES_LIB / (name + ".qss"), "r") as style_file:
        return style_file.read()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Setup logging, load config
    Logger.write_to_rotating_file("shimekiri.log")
    app.setStyleSheet(load_style())

    # Create dialog and show
    main_dialog = WatcherDialog()
    main_widget = WatcherWidget(main_dialog)
    main_dialog.show()

    sys.exit(app.exec_())
