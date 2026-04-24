import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_main import MainUI
from tab_appearance import AppearanceTab
from tab_keybindings import KeybindingsTab
from backup_manager import BackupManager

class I3EasyConfig(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("i3-EasyConfig")
        self.resize(850, 600)

        # Initialize UI
        self.ui = MainUI(self)
        self.setCentralWidget(self.ui)

        # Apply Stylesheet
        if os.path.exists("style.qss"):
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())

        # Load Modules
        self.setup_tabs()

        # Connections
        self.ui.sidebar_list.currentRowChanged.connect(self.ui.content_stack.setCurrentIndex)
        self.ui.sidebar_list.setCurrentRow(0)

    def setup_tabs(self):
        self.appearance = AppearanceTab()
        self.keybindings = KeybindingsTab()
        self.backups = BackupManager()

        self.ui.add_tab(self.appearance, "Appearance")
        self.ui.add_tab(self.keybindings, "Keybindings")
        self.ui.add_tab(self.backups, "Backup & Restore")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = I3EasyConfig()
    window.show()
    sys.exit(app.exec_())
