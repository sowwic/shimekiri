import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from shimekiri.watcher_ui import WatcherDialog
from shimekiri import Logger
from shimekiri import Config
from shimekiri import directories
from shimekiri import tray


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

    # Create tray
    tray_widget = QtWidgets.QWidget()
    tray_icon = tray.TrayIcon(QtGui.QIcon("./res/images/icons/death.png"), tray_widget)
    tray_icon.show()

    # Create dialog and show
    main_dialog = WatcherDialog()
    main_dialog.show()
    Logger.set_level(Config.get("logging.level", default=10))

    # Connect dialog to tray
    tray_icon.open_deadliner_action.triggered.connect(main_dialog.show)
    tray_icon.quit_app_action.triggered.connect(sys.exit)

    sys.exit(app.exec_())
