from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                             QSizePolicy, QSpacerItem)
from PyQt5.QtCore import pyqtSignal, Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint
from core.utils import get_icon

class Sidebar(QWidget):
    """A vertical sidebar with icon buttons for navigation."""
    
    # Signal emitted when a page button is clicked
    pageChanged = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the sidebar UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Create navigation buttons
        self.buttons = []
        
        # Home button
        self.add_button("home", "Home", 0)
        
        # Dashboard button
        self.add_button("dashboard", "Dashboard", 1)
        
        # Settings button
        self.add_button("settings", "Settings", 2)
        
        # Add vertical spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        
        # Exit button at the bottom
        self.add_button("exit", "Exit", -1)
        
        # Set the first button as active
        if self.buttons:
            self.buttons[0].setChecked(True)
    
    def add_button(self, icon_name, tooltip, page_index):
        """Add a navigation button to the sidebar."""
        button = QPushButton(self)
        button.setCheckable(True)
        button.setToolTip(tooltip)
        button.setIcon(get_icon(icon_name))
        button.setIconSize(QSize(24, 24))
        button.clicked.connect(lambda: self.handle_button_click(page_index))
        
        self.layout().addWidget(button)
        self.buttons.append(button)
        
        # Connect the button to the button group
        button.clicked.connect(lambda: self.update_button_states(button))
    
    def handle_button_click(self, page_index):
        """Handle button clicks and emit the pageChanged signal."""
        if page_index == -1:  # Exit button
            self.window().close()
        else:
            self.pageChanged.emit(page_index)
    
    def update_button_states(self, clicked_button):
        """Update the checked state of all buttons."""
        for button in self.buttons:
            if button != clicked_button and button != self.buttons[-1]:  # Exclude exit button
                button.setChecked(False) 