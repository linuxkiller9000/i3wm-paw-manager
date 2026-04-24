import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_main import MainUI
from tab_appearance import AppearanceTab
from tab_keybindings import KeybindingsTab
from backup_manager import BackupManager
from config_parser import ConfigParser
from tab_autostart import AutostartTab
from tab_raw_editor import RawEditorTab
from tab_wallpaper import WallpaperTab
from tab_app_theme import AppThemeTab

class I3EasyConfig(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("i3-EasyConfig")
        self.resize(850, 600)

        # 1. Initialize UI first
        self.ui = MainUI(self)
        self.setCentralWidget(self.ui)

        # 2. Load Modules and Tabs
        self.setup_tabs()

        # 3. Apply Stylesheet (The "Rice")
        if os.path.exists("style.qss"):
            with open("style.qss", "r") as f:
                self.setStyleSheet(f.read())
        
        # 4. Apply saved app theme if it exists
        self.load_app_theme()

        # 5. Connections (Sidebar navigation logic)
        self.ui.sidebar_list.currentRowChanged.connect(self.ui.content_stack.setCurrentIndex)
        self.ui.sidebar_list.setCurrentRow(0)

    def load_app_theme(self):
        """Load and apply saved app theme configuration"""
        import json
        theme_config_path = os.path.expanduser("~/.config/i3/app_theme.json")
        if os.path.exists(theme_config_path):
            try:
                with open(theme_config_path, "r") as f:
                    config = json.load(f)
                    # Temporarily apply theme
                    if hasattr(self.app_theme, 'generate_stylesheet'):
                        stylesheet = self.app_theme.generate_stylesheet(
                            config.get("theme", "Dark (Default)"),
                            config.get("opacity", 100) / 100.0,
                            config.get("blur", "None"),
                            config.get("bg_color", "#1e1e2e"),
                            config.get("text_color", "#cdd6f4"),
                            config.get("accent_color", "#89b4fa")
                        )
                        self.setStyleSheet(stylesheet)
            except Exception as e:
                print(f"Error loading app theme: {e}")

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
        self.wallpaper = WallpaperTab(self.parser)
        self.app_theme = AppThemeTab(self)
        self.backups = BackupManager()

        # Add tabs to the UI
        self.ui.add_tab(self.appearance, "Appearance")
        self.ui.add_tab(self.app_theme, "App Theme")
        self.ui.add_tab(self.keybindings, "Keybindings")
        self.ui.add_tab(self.autostart, "Startup Apps")
        self.ui.add_tab(self.wallpaper, "Wallpaper")
        self.ui.add_tab(self.raw_editor, "Raw Config")
        self.ui.add_tab(self.backups, "Backup & Restore")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = I3EasyConfig()
    window.show()
    sys.exit(app.exec_())
