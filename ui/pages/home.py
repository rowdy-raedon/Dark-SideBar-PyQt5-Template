from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
from PyQt5.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QRectF
from PyQt5.QtGui import QPainter, QColor, QPainterPath

class ActionCard(QFrame):
    """Interactive action card with hover animations."""
    
    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.setObjectName("actionCard")
        self.setCursor(Qt.PointingHandCursor)
        
        # Setup layout
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("""
            color: #888;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        layout.addWidget(desc_label)
        
        # Setup animations
        self._hover_animation = QPropertyAnimation(self, b"styleSheet")
        self._hover_animation.setDuration(150)
        self._hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self._base_style = """
            QFrame#actionCard {
                background-color: rgba(31, 31, 31, 0.8);
                border-radius: 4px;
                padding: 8px;
            }
        """
        
        self._hover_style = """
            QFrame#actionCard {
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

class HomePage(QWidget):
    """Home page with welcome message and quick actions."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the home page UI components."""
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
        
        # Welcome section
        welcome_frame = QFrame()
        welcome_frame.setObjectName("welcomeFrame")
        welcome_layout = QVBoxLayout(welcome_frame)
        welcome_layout.setSpacing(8)
        
        # Welcome header
        header = QLabel("Welcome to Modern PyQt5 App")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 8px;
        """)
        welcome_layout.addWidget(header)
        
        # Welcome message
        message = QLabel("Get started with these quick actions:")
        message.setStyleSheet("""
            color: #888;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 8px;
        """)
        welcome_layout.addWidget(message)
        
        content_layout.addWidget(welcome_frame)
        
        # Quick actions grid
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(16)
        
        # Action cards
        actions = [
            ("View Dashboard", "Check your analytics and statistics"),
            ("Settings", "Customize your application preferences"),
            ("Documentation", "Learn more about the application")
        ]
        
        for title, description in actions:
            card = ActionCard(title, description)
            actions_layout.addWidget(card)
        
        content_layout.addLayout(actions_layout)
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