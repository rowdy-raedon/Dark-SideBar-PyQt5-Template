from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
import os

def get_icon(name):
    """Load and return an icon from the resources directory."""
    icon_path = os.path.join("resources", "icons", f"{name}.svg")
    if not os.path.exists(icon_path):
        # Return an empty icon if the file doesn't exist
        return QIcon()
    return QIcon(icon_path)

def load_stylesheet(qss_file):
    """Load and return the contents of a QSS stylesheet file."""
    with open(qss_file, 'r') as f:
        return f.read()

class WindowDragger:
    """Helper class for implementing window dragging."""
    def __init__(self, window):
        self.window = window
        self.dragging = False
        self.offset = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.window.move(self.window.pos() + event.pos() - self.offset) 