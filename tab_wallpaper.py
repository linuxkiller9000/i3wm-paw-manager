import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from config_parser import ConfigParser
import subprocess

class WallpaperTab(QWidget):
    def __init__(self, parser: ConfigParser):
        super().__init__()
        self.parser = parser
        self.layout = QVBoxLayout(self)
        
        # Wallpaper info
        info = QLabel("Select and set a wallpaper for i3")
        self.layout.addWidget(info)
        
        # Wallpaper preview
        self.preview = QLabel()
        self.preview.setMinimumHeight(200)
        self.preview.setStyleSheet("border: 1px solid #313244;")
        self.layout.addWidget(self.preview)
        
        # Current wallpaper display
        self.current_label = QLabel("Current: None")
        self.layout.addWidget(self.current_label)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_browse = QPushButton("Browse Images")
        self.btn_browse.clicked.connect(self.browse_images)
        btn_layout.addWidget(self.btn_browse)
        
        self.btn_set = QPushButton("Set as Wallpaper")
        self.btn_set.clicked.connect(self.set_wallpaper)
        btn_layout.addWidget(self.btn_set)
        
        self.layout.addLayout(btn_layout)
        
        # Recently used wallpapers
        recent_label = QLabel("Recent Wallpapers:")
        self.layout.addWidget(recent_label)
        
        self.recent_list = QListWidget()
        self.recent_list.itemClicked.connect(self.on_recent_selected)
        self.layout.addWidget(self.recent_list)
        
        self.layout.addStretch()
        self.load_recent_wallpapers()
        self.selected_image = None
    
    def get_wallpaper_config_path(self):
        """Get the path to store wallpaper info in i3 config"""
        return os.path.expanduser("~/.config/i3/wallpaper")
    
    def browse_images(self):
        home = os.path.expanduser("~")
        image_filter = "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Wallpaper", 
            home,
            image_filter
        )
        
        if file_path:
            self.selected_image = file_path
            self.show_preview(file_path)
    
    def show_preview(self, image_path):
        """Display a preview of the selected image"""
        pixmap = QPixmap(image_path)
        scaled = pixmap.scaledToHeight(200, Qt.SmoothTransformation)
        self.preview.setPixmap(scaled)
        self.preview.setAlignment(Qt.AlignCenter)
    
    def set_wallpaper(self):
        """Set the selected wallpaper"""
        if not self.selected_image:
            QMessageBox.warning(self, "Error", "Please select an image first")
            return
        
        try:
            # Try using feh (common i3 wallpaper setter)
            subprocess.run(["feh", "--bg-scale", self.selected_image], check=True)
            
            # Save to config
            config_dir = os.path.dirname(self.get_wallpaper_config_path())
            os.makedirs(config_dir, exist_ok=True)
            
            with open(self.get_wallpaper_config_path(), "w") as f:
                f.write(self.selected_image)
            
            self.current_label.setText(f"Current: {os.path.basename(self.selected_image)}")
            self.load_recent_wallpapers()
            QMessageBox.information(self, "Success", "Wallpaper set successfully!")
            
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "feh not found. Please install feh to set wallpapers:\nsudo apt install feh")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to set wallpaper:\n{str(e)}")
    
    def load_recent_wallpapers(self):
        """Load recently used wallpapers"""
        self.recent_list.clear()
        
        wallpaper_dirs = [
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/.config/wallpapers"),
            "/usr/share/pixmaps",
        ]
        
        wallpaper_files = []
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        
        for directory in wallpaper_dirs:
            if os.path.exists(directory):
                try:
                    for filename in os.listdir(directory):
                        if filename.lower().endswith(image_extensions):
                            full_path = os.path.join(directory, filename)
                            wallpaper_files.append((filename, full_path))
                except PermissionError:
                    pass
        
        # Remove duplicates and add to list
        seen = set()
        for filename, full_path in wallpaper_files:
            if full_path not in seen:
                seen.add(full_path)
                item = QListWidgetItem(filename)
                item.setData(Qt.UserRole, full_path)
                self.recent_list.addItem(item)
    
    def on_recent_selected(self, item):
        """Handle selection from recent wallpapers"""
        image_path = item.data(Qt.UserRole)
        self.selected_image = image_path
        self.show_preview(image_path)
