from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
import os

def _project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def _qss_path(path):
    return path.replace("\\", "/")

def get_icon(name):
    """Load and return an icon from the resources directory."""
    icon_path = os.path.join(_project_root(), "resources", "icons", f"{name}.svg")
    if not os.path.exists(icon_path):
        # Return an empty icon if the file doesn't exist
        return QIcon()
    return QIcon(icon_path)

def load_stylesheet(qss_file):
    """Load and return the contents of a QSS stylesheet file."""
    if not os.path.isabs(qss_file):
        qss_file = os.path.join(_project_root(), qss_file)
    with open(qss_file, 'r') as f:
        style = f.read()
    res_dir = _qss_path(os.path.join(_project_root(), "resources"))
    style = style.replace("url(resources/", f"url({res_dir}/")
    style = style.replace("url(\"resources/", f"url(\"{res_dir}/")
    style = style.replace("url('resources/", f"url('{res_dir}/")
    return style

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
