import os
import shutil
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox

class BackupManager(QWidget):
    def __init__(self):
        super().__init__()
        self.config_path = os.path.expanduser("~/.config/i3/config")
        self.backup_path = self.config_path + ".bak"

        layout = QVBoxLayout(self)
        self.info = QLabel("Protect your configuration before making changes.")
        layout.addWidget(self.info)

        btn_backup = QPushButton("Create Backup")
        btn_backup.clicked.connect(self.create_backup)
        layout.addWidget(btn_backup)

        btn_restore = QPushButton("Restore Last Backup")
        btn_restore.clicked.connect(self.restore_backup)
        layout.addWidget(btn_restore)

    def create_backup(self):
        shutil.copy2(self.config_path, self.backup_path)
        QMessageBox.information(self, "Success", "Backup created at config.bak")

    def restore_backup(self):
        if os.path.exists(self.backup_path):
            shutil.copy2(self.backup_path, self.config_path)
            QMessageBox.information(self, "Success", "Backup restored!")
