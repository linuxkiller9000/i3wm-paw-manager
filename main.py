import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_main import MainUI
from tab_appearance import AppearanceTab
from tab_keybindings import KeybindingsTab
from backup_manager import BackupManager
from config_parser import ConfigParser
from tab_autostart import AutostartTab
from tab_raw_editor import RawEditorTab

class I3EasyConfig(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("i3-EasyConfig")
        self.resize(850, 600)

        # 1. Initialize UI first
        self.ui = MainUI(self)
        self.setCentralWidget(self.ui)

        # 2. Apply Stylesheet (The "Rice")
        if os.path.exists("style.qss"):
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())

        # 3. Load Modules and Tabs
        self.setup_tabs()

        # 4. Connections (Sidebar navigation logic)
        self.ui.sidebar_list.currentRowChanged.connect(self.ui.content_stack.setCurrentIndex)
        self.ui.sidebar_list.setCurrentRow(0)

    def setup_tabs(self):
        """
        Initializes the config engine and attaches each setting
        module to the main stacked interface.
        """
        # Create the shared engine
        self.parser = ConfigParser()

        # Initialize tabs with the parser
        self.appearance = AppearanceTab(self.parser)
        self.keybindings = KeybindingsTab(self.parser)
        self.autostart = AutostartTab(self.parser)
        self.raw_editor = RawEditorTab(self.parser)
        self.backups = BackupManager()

        # Add tabs to the UI
        self.ui.add_tab(self.appearance, "Appearance")
        self.ui.add_tab(self.keybindings, "Keybindings")
        self.ui.add_tab(self.autostart, "Startup Apps")
        self.ui.add_tab(self.raw_editor, "Raw Config")
        self.ui.add_tab(self.backups, "Backup & Restore")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = I3EasyConfig()
    window.show()
    sys.exit(app.exec_())
