import sys
from pathlib import Path
from PySide2 import QtWidgets
from shimekiri.watcher_ui import WatcherWidget, WatcherDialog
from shimekiri import Logger


def load_style(name="difness.qss"):
    stylelib = Path.cwd() / "shimekiri" / "styles"
    Logger.debug(stylelib)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Create dialog and show
    load_style()
    main_dialog = WatcherDialog()
    main_widget = WatcherWidget(main_dialog)
    main_dialog.show()

    sys.exit(app.exec_())
