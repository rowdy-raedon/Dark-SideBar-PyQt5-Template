from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QRectF
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QLinearGradient

class StatCard(QFrame):
    """Interactive statistics card with hover animations."""
    
    def __init__(self, title, value, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setCursor(Qt.PointingHandCursor)
        
        # Setup layout
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #888;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        layout.addWidget(title_label)
        
        # Setup animations
        self._hover_animation = QPropertyAnimation(self, b"styleSheet")
        self._hover_animation.setDuration(150)
        self._hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self._base_style = """
            QFrame#statCard {
                background-color: rgba(31, 31, 31, 0.8);
                border-radius: 4px;
                padding: 8px;
            }
        """
        
        self._hover_style = """
            QFrame#statCard {
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

class ContentCard(QFrame):
    """Content card with hover effect."""
    
    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.setObjectName("contentCard")
        
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
        
        # Content
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("""
            color: #888;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        layout.addWidget(content_label)
        
        # Setup shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        # Setup style
        self.setStyleSheet("""
            QFrame#contentCard {
                background-color: rgba(31, 31, 31, 0.8);
                border-radius: 4px;
                padding: 8px;
            }
        """)

class DashboardPage(QWidget):
    """Dashboard page with statistics and content cards."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the dashboard UI components."""
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
        header = QLabel("Dashboard")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 8px;
        """)
        content_layout.addWidget(header)
        
        # Statistics section
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        # Stat cards
        stats = [
            ("Active Users", "1,234"),
            ("Total Revenue", "$5,678"),
            ("Growth Rate", "+12.3%")
        ]
        
        for title, value in stats:
            card = StatCard(title, value)
            stats_layout.addWidget(card)
        
        content_layout.addLayout(stats_layout)
        
        # Content cards section
        cards_layout = QVBoxLayout()
        cards_layout.setSpacing(16)
        
        # Content cards
        cards = [
            ("Recent Activity", "Your application has been performing well with a steady increase in user engagement."),
            ("System Status", "All systems are operating normally with 99.9% uptime this month."),
            ("Updates Available", "New features and improvements are ready to be installed.")
        ]
        
        for title, content in cards:
            card = ContentCard(title, content)
            cards_layout.addWidget(card)
        
        content_layout.addLayout(cards_layout)
        content_layout.addStretch()
        
        # Set scroll area widget
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
    
    def paintEvent(self, event):
        """Custom paint event for page background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(18, 18, 18))
        gradient.setColorAt(1, QColor(24, 24, 24))
        
        # Draw background
        path = QPainterPath()
        rect = self.rect()
        path.addRect(QRectF(rect))
        painter.fillPath(path, gradient) 