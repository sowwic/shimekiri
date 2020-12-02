from PySide2 import QtWidgets


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.setToolTip("Shimekiri")

        # Tray base menu
        self.main_menu = QtWidgets.QMenu(parent)
        self.main_menu.setMaximumWidth(150)
        self.setContextMenu(self.main_menu)

        # Init UI
        self.create_actions()
        self.create_widgets()
        self.create_connections()

    def create_actions(self):
        self.open_deadliner_action = QtWidgets.QAction("Show deadliner")
        self.quit_app_action = QtWidgets.QAction("Quit")
        self.main_menu.addAction(self.open_deadliner_action)
        self.main_menu.addAction(self.quit_app_action)

    def create_widgets(self):
        pass

    def create_connections(self):
        self.activated.connect(self.on_activated)

    def on_activated(self, reason):
        if reason == self.DoubleClick:
            self.open_deadliner_action.trigger()
