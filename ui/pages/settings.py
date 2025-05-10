from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QCheckBox, QFrame, QComboBox, QPushButton, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRectF
from PyQt5.QtGui import QPainter, QColor, QPainterPath

class SettingsSection(QFrame):
    """Settings section with animated hover effect."""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsSection")
        
        # Setup layout
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        layout.addWidget(title_label)
        
        # Content container
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(8, 0, 8, 0)
        self.content_layout.setSpacing(8)
        layout.addWidget(self.content_container)
        
        # Setup animations
        self._hover_animation = QPropertyAnimation(self, b"styleSheet")
        self._hover_animation.setDuration(150)
        self._hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self._base_style = """
            QFrame#settingsSection {
                background-color: rgba(31, 31, 31, 0.8);
                border-radius: 4px;
                padding: 8px;
            }
        """
        
        self._hover_style = """
            QFrame#settingsSection {
                background-color: rgba(45, 45, 45, 0.8);
                border-radius: 4px;
                padding: 8px;
            }
        """
        
        self.setStyleSheet(self._base_style)
    
    def enterEvent(self, event):
        self._hover_animation.setStartValue(self._base_style)
        self._hover_animation.setEndValue(self._hover_style)
        self._hover_animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self._hover_animation.setStartValue(self._hover_style)
        self._hover_animation.setEndValue(self._base_style)
        self._hover_animation.start()
        super().leaveEvent(event)

class SettingsPage(QWidget):
    """Settings page with customizable options."""
    
    # Signals
    themeChanged = pyqtSignal(bool)
    fontSizeChanged = pyqtSignal(str)
    notificationsChanged = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the settings UI components."""
        # Main layout with scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)
        
        # Header
        header = QLabel("Settings")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 8px;
        """)
        content_layout.addWidget(header)
        
        # Appearance section
        appearance_section = SettingsSection("Appearance")
        
        # Theme toggle
        theme_container = QWidget()
        theme_layout = QHBoxLayout(theme_container)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        
        theme_label = QLabel("Dark Theme")
        theme_label.setStyleSheet("""
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        theme_layout.addWidget(theme_label)
        
        self.theme_toggle = QCheckBox()
        self.theme_toggle.setChecked(True)
        self.theme_toggle.stateChanged.connect(lambda state: self.themeChanged.emit(bool(state)))
        theme_layout.addWidget(self.theme_toggle)
        
        appearance_section.content_layout.addWidget(theme_container)
        
        # Font size selector
        font_container = QWidget()
        font_layout = QHBoxLayout(font_container)
        font_layout.setContentsMargins(0, 0, 0, 0)
        
        font_label = QLabel("Font Size")
        font_label.setStyleSheet("""
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        font_layout.addWidget(font_label)
        
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["Small", "Medium", "Large"])
        self.font_size_combo.setCurrentText("Medium")
        self.font_size_combo.currentTextChanged.connect(self.fontSizeChanged)
        font_layout.addWidget(self.font_size_combo)
        
        appearance_section.content_layout.addWidget(font_container)
        content_layout.addWidget(appearance_section)
        
        # Notifications section
        notifications_section = SettingsSection("Notifications")
        
        # Enable notifications toggle
        notifications_container = QWidget()
        notifications_layout = QHBoxLayout(notifications_container)
        notifications_layout.setContentsMargins(0, 0, 0, 0)
        
        notifications_label = QLabel("Enable Notifications")
        notifications_label.setStyleSheet("""
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        notifications_layout.addWidget(notifications_label)
        
        self.notifications_toggle = QCheckBox()
        self.notifications_toggle.setChecked(True)
        self.notifications_toggle.stateChanged.connect(lambda state: self.notificationsChanged.emit(bool(state)))
        notifications_layout.addWidget(self.notifications_toggle)
        
        notifications_section.content_layout.addWidget(notifications_container)
        content_layout.addWidget(notifications_section)
        
        # Add stretch to push sections to top
        content_layout.addStretch()
        
        # Set scroll area widget
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
    
    def paintEvent(self, event):
        """Custom paint event for page background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        path = QPainterPath()
        rect = self.rect()
        path.addRect(QRectF(rect))
        painter.fillPath(path, QColor(18, 18, 18))

    def save_settings(self):
        """Save the current settings."""
        # TODO: Implement settings persistence
        pass 