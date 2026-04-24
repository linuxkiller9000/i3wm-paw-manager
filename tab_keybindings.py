from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel

class KeybindingsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Active Keybindings (Read Only for now)"))

        self.table = QTableWidget(10, 2)
        self.table.setHorizontalHeaderLabels(["Shortcut", "Command"])
        layout.addWidget(self.table)
