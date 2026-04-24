from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QCheckBox, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from config_parser import ConfigParser

class AutostartTab(QWidget):
    def __init__(self, parser: ConfigParser):
        super().__init__()
        self.parser = parser
        self.layout = QVBoxLayout(self)

        # List of apps
        self.app_list = QListWidget()
        self.layout.addWidget(self.app_list)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("+ Add App")
        self.btn_add.clicked.connect(self.add_app)
        btn_layout.addWidget(self.btn_add)

        self.btn_save = QPushButton("Apply Startup Changes")
        self.btn_save.clicked.connect(self.save_changes)
        btn_layout.addWidget(self.btn_save)
        
        self.layout.addLayout(btn_layout)

        self.load_apps()

    def load_apps(self):
        self.app_list.clear()
        apps = self.parser.get_autostart_apps()
        for app in apps:
            item = QListWidgetItem(self.app_list)
            # Clean up the display name: remove # and "exec " prefix
            raw_text = app["raw"].lstrip("#").strip()
            if raw_text.startswith("exec "):
                display_text = raw_text[5:].strip()
            else:
                display_text = raw_text
            
            # Create a custom widget with a checkbox
            widget = QCheckBox(display_text)
            widget.setChecked(not app["raw"].startswith("#"))

            # Store the original file index in the checkbox for saving later
            widget.setProperty("config_index", app["index"])

            item.setSizeHint(widget.sizeHint())
            self.app_list.setItemWidget(item, widget)

    def add_app(self):
        text, ok = QInputDialog.getText(self, "Add Startup App", "Enter command to execute:")
        if ok and text:
            # Add new exec line to config
            new_line = f"exec {text}\n"
            self.parser.lines.append(new_line)
            self.load_apps()
            QMessageBox.information(self, "Success", f"Added: {text}")

    def save_changes(self):
        for i in range(self.app_list.count()):
            item = self.app_list.item(i)
            widget = self.app_list.itemWidget(item)
            index = widget.property("config_index")
            is_enabled = widget.isChecked()
            self.parser.toggle_line_comment(index, is_enabled)

        self.parser.validate_and_save()
