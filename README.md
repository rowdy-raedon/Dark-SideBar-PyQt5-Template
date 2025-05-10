# Modern PyQt5 App Template

A modern, sleek, and fully functional PyQt5 application template featuring a dark theme, fixed sidebar with icons, and a modular structure.

## Features

- 🎨 Modern Dark Theme
- 🧭 Fixed Sidebar Navigation with Icons
- 🖼️ Custom Frameless Window
- 🔄 Modular and Scalable Architecture
- 📱 Responsive Design
- ⚙️ Settings Page with Theme Toggle
- 🎯 Dashboard Example Page

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Project Structure

```
ModernAppTemplate/
├── main.py                 # Application entry point
├── ui/                     # UI components
│   ├── main_window.py     # Main window implementation
│   ├── sidebar.py         # Sidebar navigation
│   └── pages/             # Application pages
│       ├── dashboard.py   # Dashboard page
│       └── settings.py    # Settings page
├── resources/             # Application resources
│   ├── icons/            # SVG icons
│   └── style.qss         # Qt stylesheet
└── core/                 # Core functionality
    └── utils.py         # Utility functions
```

## Customization

- Theme colors can be modified in `resources/style.qss`
- Add new pages by creating a new page class in `ui/pages/` and updating the sidebar
- Icons can be replaced in `resources/icons/`

## Requirements

- Python 3.7+
- PyQt5 5.15.9+

## License

MIT License 