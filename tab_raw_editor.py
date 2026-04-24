from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from config_parser import ConfigParser

class RawEditorTab(QWidget):
    def __init__(self, parser: ConfigParser):
        super().__init__()
        self.parser = parser
        layout = QVBoxLayout(self)

        # Use PlainTextEdit for high performance on large text files
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("JetBrains Mono", 10))
        self.editor.setLineWrapMode(QPlainTextEdit.NoWrap)
        layout.addWidget(self.editor)

        self.btn_save = QPushButton("Validate & Save")
        self.btn_save.clicked.connect(self.save_config)
        layout.addWidget(self.btn_save)

        self.load_text()

    def load_text(self):
        self.parser.load_config()
        self.editor.setPlainText("".join(self.parser.lines))

    def save_config(self):
        # Update parser lines with editor content
        self.parser.lines = [line + "\n" for line in self.editor.toPlainText().split("\n")]

        success, message = self.parser.save(validate=True)
        if success:
            QMessageBox.information(self, "Success", f"Config saved. {message}")
        else:
            QMessageBox.critical(self, "Error", f"Changes not saved:\n\n{message}")
            self.load_text() # Revert to last safe state
