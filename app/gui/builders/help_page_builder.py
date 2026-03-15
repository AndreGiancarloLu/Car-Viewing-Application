from PySide6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QLabel,
                               QPushButton, QFrame, QSizePolicy)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve


class AccordionItem(QWidget):
    def __init__(self, question, answer, parent=None):
        super().__init__(parent)
        self.expanded = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 6)
        layout.setSpacing(0)

        self.toggle_btn = QPushButton(f"  ▶  {question}")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toggle_btn.setFixedHeight(52)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #e2e8f0;
                border-radius: 8px;
                text-align: left;
                padding: 0 16px;
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #334155;
            }
            QPushButton:hover { background-color: #2d3f55; }
            QPushButton:checked {
                background-color: #1a365d;
                border-color: #2b6cb0;
                color: #90cdf4;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle)
        layout.addWidget(self.toggle_btn)

        self.answer_widget = QWidget()
        self.answer_widget.setObjectName("AnswerPanel")
        self.answer_widget.setAttribute(Qt.WA_StyledBackground, True)
        self.answer_widget.setStyleSheet("""
            #AnswerPanel {
                background-color: #0f172a;
                border-radius: 0 0 8px 8px;
                border: 1px solid #334155;
                border-top: none;
            }
        """)
        self.answer_widget.setMaximumHeight(0)
        self.answer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        answer_layout = QVBoxLayout(self.answer_widget)
        answer_layout.setContentsMargins(20, 14, 20, 14)

        answer_label = QLabel(answer)
        answer_label.setWordWrap(True)
        answer_label.setStyleSheet("color: #94a3b8; font-size: 15px; line-height: 1.6;")
        answer_layout.addWidget(answer_label)

        layout.addWidget(self.answer_widget)

        self.animation = QPropertyAnimation(self.answer_widget, b"maximumHeight")
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.answer_widget.setMaximumHeight(16777215)
        self.expanded_height = self.answer_widget.sizeHint().height()
        self.answer_widget.setMaximumHeight(0)

    def toggle(self):
        self.expanded = not self.expanded
        if self.expanded:
            self.toggle_btn.setText(f"  ▼  {self.toggle_btn.text()[4:]}")
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.expanded_height)
        else:
            self.toggle_btn.setText(f"  ▶  {self.toggle_btn.text()[4:]}")
            self.animation.setStartValue(self.expanded_height)
            self.animation.setEndValue(0)
        self.animation.start()


def setup_help_page(ui):
    for child in ui.helpPage.findChildren(QLabel):
        child.deleteLater()

    root = QVBoxLayout(ui.helpPage)
    root.setContentsMargins(30, 30, 30, 30)
    root.setSpacing(20)

    title = QLabel("Help & FAQ")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 30px; font-weight: bold; color: #e2e8f0;")
    root.addWidget(title)

    subtitle = QLabel("Find answers to common questions about using the Car Viewer app.")
    subtitle.setAlignment(Qt.AlignCenter)
    subtitle.setStyleSheet("font-size: 16px; color: #64748b;")
    root.addWidget(subtitle)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet("""
        QScrollArea { border: none; background: transparent; }
        QScrollBar:vertical { background: #1f2937; width: 10px; }
        QScrollBar::handle:vertical { background: #374151; border-radius: 5px; min-height: 20px; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
    """)

    scroll_content = QWidget()
    scroll_content.setStyleSheet("background: transparent;")
    scroll_layout = QVBoxLayout(scroll_content)
    scroll_layout.setContentsMargins(0, 0, 10, 0)
    scroll_layout.setSpacing(0)

    sections = [
        {
            "heading": "Getting Started",
            "items": [
                ("What is Car Viewer?",
                 "Car Viewer is a desktop application that scrapes live car listings and automotive news from AutoDeal.com.ph, stores them locally, and lets you browse, search, filter, and compare cars."),
                ("Where does the data come from?",
                 "All car listings and news articles are scraped from AutoDeal.com.ph using Selenium. The data is stored in a local SQLite database on your machine and refreshed every time the app launches."),
                ("Why does the app take a while to start?",
                 "On launch, the app runs an ETL (Extract, Transform, Load) pipeline that scrapes the latest data from AutoDeal.com.ph and updates your local database. This can take a few minutes depending on your internet speed and how many pages are being scraped."),
            ]
        },
        {
            "heading": "Browsing Cars",
            "items": [
                ("How do I search for a specific car?",
                 "Go to the Cars page and use the search bar at the top. You can type any part of the car's name or model. Press Enter or click Search to filter the results."),
                ("How do I filter by brand or condition?",
                 "Use the Filter Bar below the search bar on the Cars page. You can select a brand from the dropdown and toggle between New, Used, or Both conditions."),
                ("Why are some cars showing 'PRICE ON REQUEST'?",
                 "Some car listings on AutoDeal.com.ph do not display a fixed price. In these cases, the app shows 'PRICE ON REQUEST' to reflect the original listing accurately."),
                ("How do I view a car's details?",
                 "Click the 'View Details' button on any car card to open its detailed page, which shows all available specifications and information."),
            ]
        },
        {
            "heading": "Comparing Cars",
            "items": [
                ("How do I compare two cars?",
                 "Go to the Compare page. Use the left panel to select your first car and the right panel to select your second car. Once both are selected, a detailed side-by-side comparison will appear at the bottom automatically."),
                ("How do I reset a car selection in the comparison?",
                 "Click the 'Change Selection' button on either side to go back to the search view and pick a different car. You can also use the 'Reset Comparison' button to clear both selections at once."),
                ("Why are some comparison fields showing 'N/A'?",
                 "Not all car listings include every specification. If a field like engine size or seating capacity wasn't available in the original listing, it will show as N/A in the comparison."),
            ]
        },
        {
            "heading": "News",
            "items": [
                ("Where do news articles come from?",
                 "News articles are scraped from the Latest Stories section of AutoDeal.com.ph and are refreshed every time the app launches."),
                ("How are news articles sorted?",
                 "Articles are sorted by date, with the most recent articles appearing first."),
                ("How do I read a full article?",
                 "Click the 'Read More' button on any news card to open the full article in the News detail view."),
            ]
        },
        {
            "heading": "Settings & Currency",
            "items": [
                ("How do I change the currency?",
                 "Go to the Settings page and select your preferred currency from the dropdown. The app supports PHP (Philippine Peso), USD (US Dollar), and CNY (Chinese Yuan). All prices will update immediately across the app."),
                ("Are currency conversions real-time?",
                 "Currency conversion rates are fixed within the app and are not fetched live. They are approximate and intended for reference only."),
            ]
        },
        {
            "heading": "Database",
            "items": [
                ("What is the Database page?",
                 "The Database page shows a raw table view of all car records currently stored in your local SQLite database. You can sort columns by clicking the headers."),
                ("Where is the database stored?",
                 "The database is stored locally at data/processed/cars.db and data/processed/news.db inside your app folder."),
            ]
        },
    ]

    for section in sections:
        section_label = QLabel(section["heading"])
        section_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #63b3ed;
            padding: 16px 0 6px 0;
        """)
        scroll_layout.addWidget(section_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #334155; min-height: 1px; max-height: 1px; margin-bottom: 8px;")
        scroll_layout.addWidget(line)

        for question, answer in section["items"]:
            item = AccordionItem(question, answer)
            scroll_layout.addWidget(item)

    scroll_layout.addStretch()
    scroll.setWidget(scroll_content)
    root.addWidget(scroll)

    return ui.helpPage