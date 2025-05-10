from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QPushButton, QStackedWidget, QFrame, QSizeGrip)
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSlot
from PyQt5.QtGui import QIcon, QResizeEvent, QMoveEvent

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.sidebar import Sidebar
from ui.pages.home import HomePage
from ui.pages.dashboard import DashboardPage
from ui.pages.settings import SettingsPage
from core.utils import WindowDragger, load_stylesheet, get_icon

class MainWindow(QMainWindow):
    """Main application window with custom title bar and sidebar."""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)  # Memory management
        
        # Window properties
        self.minimum_width = 900
        self.minimum_height = 600
        self.setMinimumSize(self.minimum_width, self.minimum_height)
        
        # Initialize window dragger
        self.window_dragger = WindowDragger(self)
        
        # Cache for frequently used widgets
        self._cached_widgets = {}
        
        # Set up the UI
        self.setup_ui()
        
        # Load and apply stylesheet
        self.load_styles()
        
        # Center the window
        self.center_window()
        
        # Initialize state
        self._is_maximized = False
    
    def setup_ui(self):
        """Initialize the main window UI components with optimized layouts."""
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Content area
        content_container = QWidget()
        content_container.setObjectName("contentContainer")
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Add custom title bar
        self.add_title_bar(content_layout)
        
        # Stacked widget for content pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("contentArea")
        
        # Initialize pages
        self.home_page = HomePage()
        self.dashboard_page = DashboardPage()
        self.settings_page = SettingsPage()
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.settings_page)
        
        content_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(content_container)
        
        # Connect sidebar signals
        self.sidebar.pageChanged.connect(self.change_page)
        
        # Add size grip for resizing
        size_grip = QSizeGrip(self)
        size_grip.setStyleSheet("background: transparent;")
        
        # Create corner widget container
        corner_widget = QWidget()
        corner_layout = QHBoxLayout(corner_widget)
        corner_layout.setContentsMargins(0, 0, 0, 0)
        corner_layout.addWidget(size_grip)
        content_layout.addWidget(corner_widget, alignment=Qt.AlignBottom | Qt.AlignRight)

    @pyqtSlot(int)
    def change_page(self, index):
        """Change the current page with smooth transition."""
        self.stacked_widget.setCurrentIndex(index)

    def add_title_bar(self, layout):
        """Add a custom title bar with optimized controls."""
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(4, 0, 0, 0)
        title_bar_layout.setSpacing(0)
        
        # Window title with icon
        title_container = QWidget()
        title_container_layout = QHBoxLayout(title_container)
        title_container_layout.setContentsMargins(4, 0, 4, 0)
        title_container_layout.setSpacing(4)
        
        window_icon = QLabel()
        window_icon.setPixmap(get_icon("app").pixmap(16, 16))
        title_container_layout.addWidget(window_icon)
        
        title = QLabel("Modern PyQt5 App")
        title.setStyleSheet("""
            font-weight: bold;
            font-size: 10px;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        title_container_layout.addWidget(title)
        title_bar_layout.addWidget(title_container)
        
        # Flexible spacer
        title_bar_layout.addStretch()
        
        # Window controls with improved hover effects
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(0)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        
        # Minimize button
        minimize_btn = QPushButton()
        minimize_btn.setObjectName("minimizeBtn")
        minimize_btn.setIcon(get_icon("minimize"))
        minimize_btn.setToolTip("Minimize")
        minimize_btn.clicked.connect(self.showMinimized)
        controls_layout.addWidget(minimize_btn)
        
        # Maximize button
        self.maximize_btn = QPushButton()
        self.maximize_btn.setObjectName("maximizeBtn")
        self.maximize_btn.setIcon(get_icon("maximize"))
        self.maximize_btn.setToolTip("Maximize")
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        controls_layout.addWidget(self.maximize_btn)
        
        # Close button
        close_btn = QPushButton()
        close_btn.setObjectName("closeBtn")
        close_btn.setIcon(get_icon("close"))
        close_btn.setToolTip("Close")
        close_btn.clicked.connect(self.close)
        controls_layout.addWidget(close_btn)
        
        title_bar_layout.addLayout(controls_layout)
        layout.addWidget(title_bar)
        
        # Connect the title bar to the window dragger
        title_bar.mousePressEvent = self.window_dragger.mousePressEvent
        title_bar.mouseReleaseEvent = self.window_dragger.mouseReleaseEvent
        title_bar.mouseMoveEvent = self.window_dragger.mouseMoveEvent

    def toggle_maximize(self):
        """Toggle between maximized and normal window state with animation."""
        if self._is_maximized:
            self.showNormal()
            self.maximize_btn.setIcon(get_icon("maximize"))
            self.maximize_btn.setToolTip("Maximize")
        else:
            self.showMaximized()
            self.maximize_btn.setIcon(get_icon("restore"))
            self.maximize_btn.setToolTip("Restore")
        self._is_maximized = not self._is_maximized

    def center_window(self):
        """Center the window on the primary screen."""
        screen = self.screen()
        screen_geometry = screen.availableGeometry()
        self.setGeometry(
            (screen_geometry.width() - self.minimum_width) // 2,
            (screen_geometry.height() - self.minimum_height) // 2,
            self.minimum_width,
            self.minimum_height
        )

    def load_styles(self):
        """Load and apply the application stylesheet."""
        style = load_stylesheet("resources/style.qss")
        if style:
            self.setStyleSheet(style)

    def resizeEvent(self, event: QResizeEvent):
        """Handle window resize events."""
        super().resizeEvent(event)
        # Update cached sizes and layouts if needed
        new_size = event.size()
        if hasattr(self, '_last_size'):
            if self._last_size != new_size:
                self._update_layout_for_size(new_size)
        self._last_size = new_size

    def _update_layout_for_size(self, size: QSize):
        """Update layouts based on new window size."""
        width = size.width()
        # Adjust sidebar visibility for small windows
        if width < 600:
            self.sidebar.setMaximumWidth(24)
        else:
            self.sidebar.setMaximumWidth(36)

    def moveEvent(self, event: QMoveEvent):
        """Handle window move events."""
        super().moveEvent(event)
        # Cache the new position
        self._last_pos = event.pos()

    def closeEvent(self, event):
        """Clean up resources before closing."""
        # Clear caches
        self._cached_widgets.clear()
        super().closeEvent(event) 