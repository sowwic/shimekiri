import sys
from PySide2 import QtWidgets
from shimekiri.watcher_ui import WatcherWidget, WatcherDialog
from shimekiri import Logger
from shimekiri import Config
from shimekiri import directories


def load_style(name="diffnes"):
    try:
        with open(directories.STYLES_LIB / (Config.get("ui_style") + ".qss"), "r") as style_file:
            return style_file.read()
    except BaseException:
        Logger.exception(f"Failed to load style {name}")
        return ""


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Setup logging, load config
    Logger.write_to_rotating_file("shimekiri.log")
    app.setStyleSheet(load_style())

    # Create dialog and show
    main_dialog = WatcherDialog()
    main_dialog.show()

    sys.exit(app.exec_())
