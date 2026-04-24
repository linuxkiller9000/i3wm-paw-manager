from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget, QFrame, QLabel
from PyQt5.QtCore import Qt

class MainUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        self.sidebar_container = QFrame()
        self.sidebar_container.setObjectName("sidebar")
        self.sidebar_container.setFixedWidth(200)

        side_layout = QVBoxLayout(self.sidebar_container)
        self.title = QLabel("i3-EASY")
        self.title.setObjectName("title")
        side_layout.addWidget(self.title)

        self.sidebar_list = QListWidget()
        self.sidebar_list.setObjectName("nav_list")
        side_layout.addWidget(self.sidebar_list)

        # Content
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_area")

        layout.addWidget(self.sidebar_container)
        layout.addWidget(self.content_stack)

    def add_tab(self, widget, name):
        self.sidebar_list.addItem(name)
        self.content_stack.addWidget(widget)
