from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QScrollArea, QSizePolicy)
from PySide6.QtCore import Qt


def make_section_heading(text):
    label = QLabel(text)
    label.setStyleSheet("font-size: 20px; font-weight: bold; color: #63b3ed; padding: 6px 0;")
    return label


def make_divider():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("background-color: #334155; min-height: 1px; max-height: 1px;")
    return line


def make_row(label_text, value_text):
    row = QWidget()
    row.setStyleSheet("background: transparent;")
    layout = QHBoxLayout(row)
    layout.setContentsMargins(16, 10, 16, 10)
    layout.setSpacing(24)

    label = QLabel(label_text)
    label.setFixedWidth(220)
    label.setStyleSheet("color: #94a3b8; font-size: 15px;")

    value = QLabel(value_text)
    value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    value.setStyleSheet("color: #e2e8f0; font-size: 15px;")

    layout.addWidget(label)
    layout.addWidget(value)
    return row


def make_tag(text, color):
    tag = QLabel(text)
    tag.setAlignment(Qt.AlignCenter)
    tag.setFixedHeight(34)
    tag.setStyleSheet(f"""
        background-color: {color};
        color: white;
        border-radius: 8px;
        padding: 4px 16px;
        font-size: 14px;
        font-weight: bold;
    """)
    return tag


def setup_about_page(ui):
    for child in ui.aboutPage.findChildren(QLabel):
        child.deleteLater()

    root = QVBoxLayout(ui.aboutPage)
    root.setContentsMargins(30, 30, 30, 30)
    root.setSpacing(20)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet("""
        QScrollArea { border: none; background: transparent; }
        QScrollBar:vertical { background: #1f2937; width: 10px; }
        QScrollBar::handle:vertical { background: #374151; border-radius: 5px; min-height: 20px; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
    """)

    content = QWidget()
    content.setStyleSheet("background: transparent;")
    layout = QVBoxLayout(content)
    layout.setContentsMargins(0, 0, 10, 0)
    layout.setSpacing(20)

    # ── Banner ──
    banner = QWidget()
    banner.setObjectName("Banner")
    banner.setAttribute(Qt.WA_StyledBackground, True)
    banner.setStyleSheet("""
        #Banner {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #1a365d, stop:1 #2b6cb0);
            border-radius: 14px;
        }
    """)
    banner_layout = QVBoxLayout(banner)
    banner_layout.setContentsMargins(30, 30, 30, 30)
    banner_layout.setSpacing(10)

    app_name = QLabel("Car Viewer")
    app_name.setAlignment(Qt.AlignCenter)
    app_name.setStyleSheet("font-size: 38px; font-weight: bold; color: #e2e8f0;")
    banner_layout.addWidget(app_name)

    app_version = QLabel("Version 1.0.0")
    app_version.setAlignment(Qt.AlignCenter)
    app_version.setStyleSheet("font-size: 16px; color: #90cdf4;")
    banner_layout.addWidget(app_version)

    app_desc = QLabel(
        "A desktop application for browsing, searching, and comparing car listings\n"
        "and automotive news sourced live from AutoDeal.com.ph."
    )
    app_desc.setAlignment(Qt.AlignCenter)
    app_desc.setWordWrap(True)
    app_desc.setStyleSheet("font-size: 15px; color: #cbd5e0; padding-top: 8px;")
    banner_layout.addWidget(app_desc)

    layout.addWidget(banner)

    # ── App Info ──
    layout.addWidget(make_section_heading("Application Info"))
    layout.addWidget(make_divider())

    info_card = QWidget()
    info_card.setObjectName("Card")
    info_card.setAttribute(Qt.WA_StyledBackground, True)
    info_card.setStyleSheet("#Card { background-color: #1e293b; border-radius: 10px; }")
    info_layout = QVBoxLayout(info_card)
    info_layout.setContentsMargins(0, 8, 0, 8)
    info_layout.setSpacing(0)

    for label, value in [
        ("Application Name", "Car Viewer"),
        ("Version", "1.0.0"),
        ("Developer", "AndreGiancarloLu"),
        ("Language", "Python 3"),
        ("UI Framework", "PySide6 (Qt for Python)"),
        ("Database", "SQLite"),
        ("Scraping Engine", "Selenium + Firefox (headless)"),
        ("Data Source", "AutoDeal.com.ph"),
    ]:
        info_layout.addWidget(make_row(label, value))
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #334155; min-height: 1px; max-height: 1px; margin: 0 8px;")
        info_layout.addWidget(sep)

    layout.addWidget(info_card)

    # ── Tech Stack ──
    layout.addWidget(make_section_heading("Tech Stack"))
    layout.addWidget(make_divider())

    tags_widget = QWidget()
    tags_widget.setStyleSheet("background: transparent;")
    tags_layout = QHBoxLayout(tags_widget)
    tags_layout.setContentsMargins(0, 10, 0, 10)
    tags_layout.setSpacing(12)
    tags_layout.setAlignment(Qt.AlignLeft)

    for name, color in [
        ("Python 3", "#3b82f6"),
        ("PySide6", "#8b5cf6"),
        ("Selenium", "#059669"),
        ("BeautifulSoup4", "#dc2626"),
        ("Requests", "#0891b2"),
        ("SQLite", "#d97706"),
        ("Qt Custom Widgets", "#7c3aed"),
    ]:
        tags_layout.addWidget(make_tag(name, color))
    tags_layout.addStretch()

    layout.addWidget(tags_widget)

    tech_card = QWidget()
    tech_card.setObjectName("Card")
    tech_card.setAttribute(Qt.WA_StyledBackground, True)
    tech_card.setStyleSheet("#Card { background-color: #1e293b; border-radius: 10px; }")
    tech_layout = QVBoxLayout(tech_card)
    tech_layout.setContentsMargins(0, 8, 0, 8)
    tech_layout.setSpacing(0)

    for label, value in [
        ("PySide6", "UI framework: all windows, widgets, and layouts"),
        ("Selenium", "Headless Firefox browser: scrapes car listings and news from AutoDeal.com.ph"),
        ("BeautifulSoup4", "HTML parser: extracts detailed car specs from individual listing pages"),
        ("Requests", "HTTP client: downloads car and news images for local caching"),
        ("SQLite", "Local database: stores all scraped car and news data"),
        ("Qt Custom Widgets", "KhamisiKibet's library: provides the sliding menus and animated navigation"),
    ]:
        tech_layout.addWidget(make_row(label, value))
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #334155; min-height: 1px; max-height: 1px; margin: 0 8px;")
        tech_layout.addWidget(sep)

    layout.addWidget(tech_card)

    # ── Disclaimer ──
    disclaimer = QLabel(
        "Disclaimer: This app is for personal and educational use only. "
        "Car listings, prices, and news are scraped from AutoDeal.com.ph and may not reflect "
        "current real-world availability or pricing. Always verify with the official source."
    )
    disclaimer.setWordWrap(True)
    disclaimer.setAlignment(Qt.AlignCenter)
    disclaimer.setStyleSheet("""
        color: #64748b;
        font-size: 13px;
        padding: 14px 20px;
        background-color: #1e293b;
        border-radius: 8px;
        border: 1px solid #334155;
    """)
    layout.addWidget(disclaimer)
    layout.addStretch()

    scroll.setWidget(content)
    root.addWidget(scroll)

    return ui.aboutPage