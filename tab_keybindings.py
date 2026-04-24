from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QHeaderView, QMessageBox, QInputDialog, QDialog, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from config_parser import ConfigParser

class KeyCaptureDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Capture Shortcut")
        self.setModal(True)
        self.setFixedSize(320, 140)

        layout = QVBoxLayout(self)
        label = QLabel("Press the shortcut keys now\n(press Esc to cancel)")
        label.setWordWrap(True)
        layout.addWidget(label)

        self.display = QLabel("Waiting for input...")
        layout.addWidget(self.display)

        self.shortcut = None

    def showEvent(self, event):
        super().showEvent(event)
        self.grabKeyboard()

    def closeEvent(self, event):
        self.releaseKeyboard()
        super().closeEvent(event)

    def reject(self):
        self.releaseKeyboard()
        super().reject()

    def accept(self):
        self.releaseKeyboard()
        super().accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.reject()
            return

        modifiers = event.modifiers()
        key = event.key()

        if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta, Qt.Key_Super, Qt.Key_AltGr):
            return

        sequence = QKeySequence(modifiers | key).toString(QKeySequence.PortableText)
        if sequence:
            normalized = sequence
            normalized = normalized.replace("Meta", "$mod").replace("Super", "$mod")
            normalized = normalized.replace("Ctrl", "Control")
            normalized = normalized.replace("Alt", "Mod1") if "Mod1" not in normalized else normalized
            self.shortcut = normalized
            self.display.setText(f"Captured: {normalized}")
            self.accept()

class KeybindingsTab(QWidget):
    def __init__(self, parser: ConfigParser):
        super().__init__()
        self.parser = parser
        self.layout = QVBoxLayout(self)

        # Top Bar: Search
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search bindings (e.g., Return, Firefox)...")
        self.search_bar.textChanged.connect(self.filter_table)
        self.layout.addWidget(self.search_bar)

        # Main Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Description", "Shortcut", "Command"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        # Bottom Bar: Actions
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("+ Add Binding")
        self.btn_add.clicked.connect(self.add_binding)
        btn_layout.addWidget(self.btn_add)

        self.btn_delete = QPushButton("Delete Selected")
        self.btn_delete.clicked.connect(self.delete_selected)
        btn_layout.addWidget(self.btn_delete)

        self.btn_save = QPushButton("Save Keybindings")
        self.btn_save.clicked.connect(self.save_changes)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        self.layout.addLayout(btn_layout)

        self.load_bindings()

    def load_bindings(self):
        self.table.setRowCount(0)
        self.bind_references = [] # Store original line indexes to safely update them later

        for i, line in enumerate(self.parser.lines):
            stripped = line.strip()
            if stripped.startswith("bindsym "):
                # Try to get the comment from the line above as a description
                desc = "Custom Binding"
                if i > 0 and self.parser.lines[i-1].strip().startswith("#"):
                    desc = self.parser.lines[i-1].strip().lstrip("#").strip()

                # Parse: bindsym $mod+Return exec alacritty
                parts = stripped.split(" ", 2)
                if len(parts) >= 3:
                    shortcut = parts[1]
                    command = parts[2]

                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    self.table.setItem(row, 0, QTableWidgetItem(desc))
                    self.table.setItem(row, 1, QTableWidgetItem(shortcut))
                    self.table.setItem(row, 2, QTableWidgetItem(command))

                    self.bind_references.append(i) # Keep track of where this bind lives in the config

    def filter_table(self, text):
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if text.lower() in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

    def add_binding(self):
        dialog = KeyCaptureDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.shortcut:
            shortcut = dialog.shortcut
            command, ok2 = QInputDialog.getText(self, "Add Keybinding", "Enter command to execute:")
            if ok2 and command:
                new_line = f"bindsym {shortcut} {command}\n"
                self.parser.lines.append(new_line)
                self.load_bindings()
                QMessageBox.information(self, "Success", f"Added: {shortcut} → {command}")

    def delete_selected(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            # We comment it out in the parser to be safe, instead of deleting
            config_index = self.bind_references[current_row]
            self.parser.lines[config_index] = "# " + self.parser.lines[config_index]
            self.table.removeRow(current_row)
            self.bind_references.pop(current_row)

    def save_changes(self):
        # Update existing binds in memory
        for row in range(self.table.rowCount()):
            config_index = self.bind_references[row]
            shortcut = self.table.item(row, 1).text()
            command = self.table.item(row, 2).text()
            self.parser.lines[config_index] = f"bindsym {shortcut} {command}\n"

        success, message = self.parser.validate_and_save()
        if success:
            QMessageBox.information(self, "Success", "Keybindings updated and i3 reloaded!")
        else:
            QMessageBox.critical(self, "Error", f"Failed to reload i3:\n{message}")
            self.parser.load_config() # Revert to last safe state

