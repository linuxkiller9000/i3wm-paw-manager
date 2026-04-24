from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSlider, QComboBox, QPushButton, QGroupBox, QSpinBox, QMessageBox)
from PyQt5.QtCore import Qt
from config_parser import ConfigParser

class AppearanceTab(QWidget):
    def __init__(self, parser: ConfigParser):
        super().__init__()
        self.parser = parser
        self.layout = QVBoxLayout(self)

        self.setup_gaps_section()
        self.setup_window_section()
        self.layout.addStretch()

        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.confirm_changes)
        self.layout.addWidget(self.btn_ok)

        self.load_current_values()
        self.connect_live_preview()

    def setup_gaps_section(self):
        group = QGroupBox("i3 Gaps")
        group_layout = QVBoxLayout()

        # Inner Gaps
        inner_layout = QHBoxLayout()
        inner_layout.addWidget(QLabel("Inner Gaps:"))
        self.spin_inner = QSpinBox()
        self.spin_inner.setRange(0, 100)
        inner_layout.addWidget(self.spin_inner)
        group_layout.addLayout(inner_layout)

        # Outer Gaps
        outer_layout = QHBoxLayout()
        outer_layout.addWidget(QLabel("Outer Gaps:"))
        self.spin_outer = QSpinBox()
        self.spin_outer.setRange(0, 100)
        outer_layout.addWidget(self.spin_outer)
        group_layout.addLayout(outer_layout)

        group.setLayout(group_layout)
        self.layout.addWidget(group)

    def setup_window_section(self):
        group = QGroupBox("Window Rules")
        group_layout = QVBoxLayout()

        # Border Style
        border_layout = QHBoxLayout()
        border_layout.addWidget(QLabel("Default Border:"))
        self.combo_border = QComboBox()
        self.combo_border.addItems(["pixel", "normal", "none"])
        border_layout.addWidget(self.combo_border)

        self.spin_border_size = QSpinBox()
        self.spin_border_size.setRange(0, 10)
        self.spin_border_size.setSuffix(" px")
        border_layout.addWidget(self.spin_border_size)
        group_layout.addLayout(border_layout)

        group.setLayout(group_layout)
        self.layout.addWidget(group)

    def load_current_values(self):
        # We manually scan the lines to find current values
        for line in self.parser.lines:
            stripped = line.strip()
            if stripped.startswith("gaps inner"):
                try: self.spin_inner.setValue(int(stripped.split()[-1]))
                except ValueError: pass

            elif stripped.startswith("gaps outer"):
                try: self.spin_outer.setValue(int(stripped.split()[-1]))
                except ValueError: pass

            elif stripped.startswith("default_border") or stripped.startswith("new_window"):
                parts = stripped.split()
                if len(parts) >= 2:
                    style = parts[1]
                    index = self.combo_border.findText(style)
                    if index >= 0: self.combo_border.setCurrentIndex(index)
                if len(parts) == 3:
                    try: self.spin_border_size.setValue(int(parts[2]))
                    except ValueError: pass

    def connect_live_preview(self):
        self.spin_inner.valueChanged.connect(self.update_parser_lines)
        self.spin_outer.valueChanged.connect(self.update_parser_lines)
        self.combo_border.currentIndexChanged.connect(self.update_parser_lines)
        self.spin_border_size.valueChanged.connect(self.update_parser_lines)

    def update_parser_lines(self):
        inner_val = self.spin_inner.value()
        outer_val = self.spin_outer.value()
        border_style = self.combo_border.currentText()
        border_size = self.spin_border_size.value()

        def replace_or_add(prefix, new_line):
            found = False
            for i, line in enumerate(self.parser.lines):
                if line.strip().startswith(prefix):
                    self.parser.lines[i] = new_line + "\n"
                    found = True
                    break
            if not found:
                self.parser.lines.append(new_line + "\n")

        replace_or_add("gaps inner", f"gaps inner {inner_val}")
        replace_or_add("gaps outer", f"gaps outer {outer_val}")

        if border_style == "pixel" or border_style == "normal":
            replace_or_add("default_border", f"default_border {border_style} {border_size}")
            replace_or_add("new_window", f"new_window {border_style} {border_size}") # legacy i3 support
        else:
            replace_or_add("default_border", "default_border none")
            replace_or_add("new_window", "new_window none")

    def confirm_changes(self):
        self.update_parser_lines()
        success, message = self.parser.validate_and_save()
        if success:
            QMessageBox.information(self, "Success", "Changes saved to i3 config.")
        else:
            QMessageBox.critical(self, "Error", f"Failed to save config:\n{message}")
