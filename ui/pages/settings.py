from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QCheckBox, QFrame, QComboBox, QPushButton, QScrollArea,
                             QSpinBox, QLineEdit)
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
    
    # Signals for settings changes
    themeChanged = pyqtSignal(bool)
    fontSizeChanged = pyqtSignal(str)
    notificationsChanged = pyqtSignal(bool)
    languageChanged = pyqtSignal(str)
    autoSaveChanged = pyqtSignal(int)
    apiKeyChanged = pyqtSignal(str)
    customThemeChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def create_setting_row(self, label_text, widget):
        """Helper method to create a consistent setting row layout."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(label_text)
        label.setStyleSheet("""
            background-color: rgba(31, 31, 31, 0.8);
            border-radius: 4px;
            padding: 4px;
        """)
        layout.addWidget(label)
        layout.addWidget(widget)
        
        return container

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
        
        # SECTION 1: Appearance
        appearance_section = SettingsSection("Appearance")
        
        # Theme toggle
        self.theme_toggle = QCheckBox()
        self.theme_toggle.setChecked(True)
        self.theme_toggle.stateChanged.connect(lambda state: self.themeChanged.emit(bool(state)))
        appearance_section.content_layout.addWidget(
            self.create_setting_row("Dark Theme", self.theme_toggle)
        )
        
        # Font size selector
        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(["Small", "Medium", "Large"])
        self.font_size_combo.setCurrentText("Medium")
        self.font_size_combo.currentTextChanged.connect(self.fontSizeChanged)
        appearance_section.content_layout.addWidget(
            self.create_setting_row("Font Size", self.font_size_combo)
        )
        
        # Language selector
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Spanish", "French", "German", "Chinese"])
        self.language_combo.currentTextChanged.connect(self.languageChanged)
        appearance_section.content_layout.addWidget(
            self.create_setting_row("Language", self.language_combo)
        )
        
        content_layout.addWidget(appearance_section)
        
        # SECTION 2: User Preferences
        preferences_section = SettingsSection("User Preferences")
        
        # Auto-save interval
        self.auto_save_spin = QSpinBox()
        self.auto_save_spin.setRange(1, 60)
        self.auto_save_spin.setValue(5)
        self.auto_save_spin.setSuffix(" minutes")
        self.auto_save_spin.valueChanged.connect(self.autoSaveChanged)
        preferences_section.content_layout.addWidget(
            self.create_setting_row("Auto-save Interval", self.auto_save_spin)
        )
        
        # Notifications toggle
        self.notifications_toggle = QCheckBox()
        self.notifications_toggle.setChecked(True)
        self.notifications_toggle.stateChanged.connect(lambda state: self.notificationsChanged.emit(bool(state)))
        preferences_section.content_layout.addWidget(
            self.create_setting_row("Enable Notifications", self.notifications_toggle)
        )
        
        content_layout.addWidget(preferences_section)
        
        # SECTION 3: Advanced Settings
        advanced_section = SettingsSection("Advanced Settings")
        
        # API Key input
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your API key")
        self.api_key_input.textChanged.connect(self.apiKeyChanged)
        advanced_section.content_layout.addWidget(
            self.create_setting_row("API Key", self.api_key_input)
        )
        
        # Debug mode
        self.debug_mode = QCheckBox()
        advanced_section.content_layout.addWidget(
            self.create_setting_row("Debug Mode", self.debug_mode)
        )
        
        content_layout.addWidget(advanced_section)
        
        # SECTION 4: Custom Themes
        themes_section = SettingsSection("Custom Themes")
        
        # Theme selector
        self.custom_theme_combo = QComboBox()
        self.custom_theme_combo.addItems([
            "Default Dark",
            "Monokai",
            "Solarized Dark",
            "Nord",
            "Dracula"
        ])
        self.custom_theme_combo.currentTextChanged.connect(self.customThemeChanged)
        themes_section.content_layout.addWidget(
            self.create_setting_row("Theme Preset", self.custom_theme_combo)
        )
        
        # Accent color
        self.accent_color_combo = QComboBox()
        self.accent_color_combo.addItems([
            "Blue",
            "Green",
            "Purple",
            "Orange",
            "Pink"
        ])
        themes_section.content_layout.addWidget(
            self.create_setting_row("Accent Color", self.accent_color_combo)
        )
        
        content_layout.addWidget(themes_section)
        
        # Add stretch to push sections to top
        content_layout.addStretch()
        
        # Add save button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1084E2;
            }
            QPushButton:pressed {
                background-color: #006CC1;
            }
        """)
        content_layout.addWidget(self.save_button)
        
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
        # Example implementation structure:
        settings = {
            'theme': {
                'dark_mode': self.theme_toggle.isChecked(),
                'font_size': self.font_size_combo.currentText(),
                'language': self.language_combo.currentText(),
                'custom_theme': self.custom_theme_combo.currentText(),
                'accent_color': self.accent_color_combo.currentText()
            },
            'preferences': {
                'auto_save_interval': self.auto_save_spin.value(),
                'notifications_enabled': self.notifications_toggle.isChecked()
            },
            'advanced': {
                'api_key': self.api_key_input.text(),
                'debug_mode': self.debug_mode.isChecked()
            }
        }
        # TODO: Save settings to file/database
        pass 