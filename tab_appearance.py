from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from config_parser import ConfigParser

class AppearanceTab(QWidget):
    def __init__(self):
        super().__init__()
        self.parser = ConfigParser()
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Inner Gaps Size"))
        self.gap_slider = QSlider(Qt.Horizontal)
        self.gap_slider.setRange(0, 50)

        # Load current value
        current_gap = self.parser.get_value(r"gaps inner (\d+)")
        self.gap_slider.setValue(int(current_gap) if current_gap else 0)

        self.gap_slider.valueChanged.connect(self.update_gaps)
        layout.addWidget(self.gap_slider)
        layout.addStretch()

    def update_gaps(self, value):
        self.parser.update_value(r"gaps inner \d+", f"gaps inner {value}")
