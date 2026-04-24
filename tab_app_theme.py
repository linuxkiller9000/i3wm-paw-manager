import os
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
                             QSlider, QPushButton, QGroupBox, QColorDialog, QSpinBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class AppThemeTab(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.layout = QVBoxLayout(self)
        self.theme_config_path = os.path.expanduser("~/.config/i3/app_theme.json")
        
        # Load current theme settings
        self.load_theme_config()
        
        # Theme Selection
        self.setup_theme_section()
        
        # Transparency/Opacity
        self.setup_transparency_section()
        
        # Custom Colors
        self.setup_custom_colors_section()
        
        # Apply Button
        self.btn_apply = QPushButton("Apply Theme Changes")
        self.btn_apply.clicked.connect(self.apply_theme)
        self.layout.addWidget(self.btn_apply)
        
        self.layout.addStretch()

    def setup_theme_section(self):
        """Setup theme selection group"""
        group = QGroupBox("App Theme")
        group_layout = QVBoxLayout()
        
        # Theme selector
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Select Theme:"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Dark (Default)", "Light", "Custom"])
        self.combo_theme.currentTextChanged.connect(self.on_theme_changed)
        theme_layout.addWidget(self.combo_theme)
        group_layout.addLayout(theme_layout)
        
        # Description
        self.theme_desc = QLabel("Dark theme with Catppuccin Mocha colors")
        self.theme_desc.setWordWrap(True)
        group_layout.addWidget(self.theme_desc)
        
        group.setLayout(group_layout)
        self.layout.addWidget(group)

    def setup_transparency_section(self):
        """Setup transparency and blur controls"""
        group = QGroupBox("Transparency & Effects")
        group_layout = QVBoxLayout()
        
        # Opacity/Transparency
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("Opacity:"))
        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(50, 100)
        self.slider_opacity.setValue(100)
        self.slider_opacity.setTickPosition(QSlider.TicksBelow)
        self.slider_opacity.setTickInterval(10)
        opacity_layout.addWidget(self.slider_opacity)
        self.label_opacity = QLabel("100%")
        opacity_layout.addWidget(self.label_opacity)
        self.slider_opacity.valueChanged.connect(self.update_opacity_label)
        group_layout.addLayout(opacity_layout)
        
        # Background blur (simulated with color overlay)
        blur_layout = QHBoxLayout()
        blur_layout.addWidget(QLabel("Background Blur:"))
        self.combo_blur = QComboBox()
        self.combo_blur.addItems(["None", "Light", "Medium", "Strong"])
        blur_layout.addWidget(self.combo_blur)
        group_layout.addLayout(blur_layout)
        
        group.setLayout(group_layout)
        self.layout.addWidget(group)

    def setup_custom_colors_section(self):
        """Setup custom color selection"""
        group = QGroupBox("Custom Colors")
        group_layout = QVBoxLayout()
        
        # Background color
        bg_layout = QHBoxLayout()
        bg_layout.addWidget(QLabel("Background Color:"))
        self.btn_bg_color = QPushButton("Choose Color")
        self.btn_bg_color.setStyleSheet("background-color: #1e1e2e;")
        self.btn_bg_color.clicked.connect(self.choose_bg_color)
        bg_layout.addWidget(self.btn_bg_color)
        self.label_bg_color = QLabel("#1e1e2e")
        bg_layout.addWidget(self.label_bg_color)
        group_layout.addLayout(bg_layout)
        
        # Text color
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("Text Color:"))
        self.btn_text_color = QPushButton("Choose Color")
        self.btn_text_color.setStyleSheet("background-color: #cdd6f4; color: #1e1e2e;")
        self.btn_text_color.clicked.connect(self.choose_text_color)
        text_layout.addWidget(self.btn_text_color)
        self.label_text_color = QLabel("#cdd6f4")
        text_layout.addWidget(self.label_text_color)
        group_layout.addLayout(text_layout)
        
        # Accent color
        accent_layout = QHBoxLayout()
        accent_layout.addWidget(QLabel("Accent Color:"))
        self.btn_accent_color = QPushButton("Choose Color")
        self.btn_accent_color.setStyleSheet("background-color: #89b4fa;")
        self.btn_accent_color.clicked.connect(self.choose_accent_color)
        accent_layout.addWidget(self.btn_accent_color)
        self.label_accent_color = QLabel("#89b4fa")
        accent_layout.addWidget(self.label_accent_color)
        group_layout.addLayout(accent_layout)
        
        # Reset to defaults
        self.btn_reset = QPushButton("Reset to Defaults")
        self.btn_reset.clicked.connect(self.reset_to_defaults)
        group_layout.addWidget(self.btn_reset)
        
        group.setLayout(group_layout)
        self.layout.addWidget(group)

    def on_theme_changed(self, theme_name):
        """Update description based on selected theme"""
        descriptions = {
            "Dark (Default)": "Dark theme with Catppuccin Mocha colors",
            "Light": "Light theme with clean, minimalist design",
            "Custom": "Create your own theme with custom colors"
        }
        self.theme_desc.setText(descriptions.get(theme_name, ""))

    def update_opacity_label(self, value):
        """Update opacity percentage label"""
        self.label_opacity.setText(f"{value}%")

    def choose_bg_color(self):
        """Open color picker for background color"""
        current_color = QColor(self.label_bg_color.text())
        color = QColorDialog.getColor(current_color, self, "Choose Background Color")
        if color.isValid():
            hex_color = color.name()
            self.label_bg_color.setText(hex_color)
            self.btn_bg_color.setStyleSheet(f"background-color: {hex_color};")

    def choose_text_color(self):
        """Open color picker for text color"""
        current_color = QColor(self.label_text_color.text())
        color = QColorDialog.getColor(current_color, self, "Choose Text Color")
        if color.isValid():
            hex_color = color.name()
            self.label_text_color.setText(hex_color)
            self.btn_text_color.setStyleSheet(f"background-color: {hex_color};")

    def choose_accent_color(self):
        """Open color picker for accent color"""
        current_color = QColor(self.label_accent_color.text())
        color = QColorDialog.getColor(current_color, self, "Choose Accent Color")
        if color.isValid():
            hex_color = color.name()
            self.label_accent_color.setText(hex_color)
            self.btn_accent_color.setStyleSheet(f"background-color: {hex_color};")

    def load_theme_config(self):
        """Load saved theme configuration"""
        if os.path.exists(self.theme_config_path):
            try:
                with open(self.theme_config_path, "r") as f:
                    config = json.load(f)
                    # Load values from config
                    self.theme_name = config.get("theme", "Dark (Default)")
                    self.opacity = config.get("opacity", 100)
                    self.blur = config.get("blur", "None")
                    self.bg_color = config.get("bg_color", "#1e1e2e")
                    self.text_color = config.get("text_color", "#cdd6f4")
                    self.accent_color = config.get("accent_color", "#89b4fa")
                    return
            except Exception as e:
                print(f"Error loading theme config: {e}")
        
        # Default values
        self.theme_name = "Dark (Default)"
        self.opacity = 100
        self.blur = "None"
        self.bg_color = "#1e1e2e"
        self.text_color = "#cdd6f4"
        self.accent_color = "#89b4fa"

    def save_theme_config(self):
        """Save theme configuration to file"""
        config = {
            "theme": self.combo_theme.currentText(),
            "opacity": self.slider_opacity.value(),
            "blur": self.combo_blur.currentText(),
            "bg_color": self.label_bg_color.text(),
            "text_color": self.label_text_color.text(),
            "accent_color": self.label_accent_color.text()
        }
        
        os.makedirs(os.path.dirname(self.theme_config_path), exist_ok=True)
        with open(self.theme_config_path, "w") as f:
            json.dump(config, f, indent=2)

    def apply_theme(self):
        """Apply the selected theme to the app"""
        theme = self.combo_theme.currentText()
        opacity = self.slider_opacity.value() / 100.0
        blur = self.combo_blur.currentText()
        bg_color = self.label_bg_color.text()
        text_color = self.label_text_color.text()
        accent_color = self.label_accent_color.text()
        
        # Generate stylesheet
        stylesheet = self.generate_stylesheet(theme, opacity, blur, bg_color, text_color, accent_color)
        
        # Apply to parent window
        self.parent_window.setStyleSheet(stylesheet)
        
        # Save configuration
        self.save_theme_config()
        
        QMessageBox.information(self, "Success", "Theme applied successfully!")

    def generate_stylesheet(self, theme, opacity, blur, bg_color, text_color, accent_color):
        """Generate QSS stylesheet based on theme settings"""
        opacity_percent = int(opacity * 100)
        
        # Base stylesheet
        stylesheet = f"""
QWidget {{
    background-color: {bg_color};
    color: {text_color};
    font-family: "JetBrains Mono", "Sans";
}}

#sidebar {{
    background-color: {self.darken_color(bg_color, 20)};
    border-right: 1px solid {accent_color};
}}

#title {{
    font-weight: bold;
    font-size: 18px;
    padding: 20px;
    color: {accent_color};
}}

QListWidget {{
    border: none;
    background: transparent;
}}

QListWidget::item {{
    padding: 10px;
    border-radius: 5px;
}}

QListWidget::item:selected {{
    background-color: {accent_color};
    color: {bg_color};
}}

QPushButton {{
    background-color: {accent_color};
    color: {bg_color};
    border-radius: 5px;
    padding: 8px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {self.lighten_color(accent_color, 10)};
}}

QGroupBox {{
    color: {text_color};
    border: 1px solid {accent_color};
    border-radius: 5px;
    padding-top: 10px;
    margin-top: 10px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}}

QSlider::handle:horizontal {{
    background-color: {accent_color};
}}

QComboBox {{
    background-color: {self.darken_color(bg_color, 10)};
    color: {text_color};
    border: 1px solid {accent_color};
    padding: 5px;
    border-radius: 3px;
}}

QComboBox:hover {{
    border: 1px solid {self.lighten_color(accent_color, 10)};
}}

QLineEdit {{
    background-color: {self.darken_color(bg_color, 10)};
    color: {text_color};
    border: 1px solid {accent_color};
    padding: 5px;
    border-radius: 3px;
}}

QTableWidget {{
    background-color: {self.darken_color(bg_color, 10)};
    alternate-background-color: {bg_color};
}}

QTableWidget::item {{
    padding: 5px;
}}

QPlainTextEdit {{
    background-color: {self.darken_color(bg_color, 15)};
    color: {text_color};
    border: 1px solid {accent_color};
}}

QCheckBox {{
    color: {text_color};
}}

QCheckBox::indicator {{
    border: 1px solid {accent_color};
    border-radius: 3px;
    background-color: transparent;
}}

QCheckBox::indicator:checked {{
    background-color: {accent_color};
}}
"""
        return stylesheet

    def darken_color(self, hex_color, amount):
        """Darken a hex color by a given amount"""
        color = QColor(hex_color)
        color = color.darker(100 + amount)
        return color.name()

    def lighten_color(self, hex_color, amount):
        """Lighten a hex color by a given amount"""
        color = QColor(hex_color)
        color = color.lighter(100 + amount)
        return color.name()

    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.combo_theme.setCurrentText("Dark (Default)")
        self.slider_opacity.setValue(100)
        self.combo_blur.setCurrentText("None")
        self.label_bg_color.setText("#1e1e2e")
        self.btn_bg_color.setStyleSheet("background-color: #1e1e2e;")
        self.label_text_color.setText("#cdd6f4")
        self.btn_text_color.setStyleSheet("background-color: #cdd6f4; color: #1e1e2e;")
        self.label_accent_color.setText("#89b4fa")
        self.btn_accent_color.setStyleSheet("background-color: #89b4fa;")
        QMessageBox.information(self, "Reset", "Theme reset to defaults")
