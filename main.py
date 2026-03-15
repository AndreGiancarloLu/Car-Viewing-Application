import os
import sys

from app.gui.ui_interface import *
from app.gui.components.custom_widgets import SlideMenu, AnimatedStackedWidget, ButtonGroup
from PySide6.QtCore import QEasingCurve
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
from app.etl.etl import run_etl
from app.gui.utils.db_reader import fetch_car_data, fetch_news_data
from app.gui.builders.cars_page_builder import setup_cars_page, show_car_details
from app.gui.builders.news_page_builder import setup_news_page, show_news_details
from app.gui.builders.comparison_page_builder import setup_comparison_page
from app.gui.builders.home_page_builder import setup_home_page
from app.gui.builders.help_page_builder import setup_help_page
from app.gui.builders.about_page_builder import setup_about_page


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_signals()

        run_etl()
        self.ui.setup_database_table_view()

        car_data = fetch_car_data()
        news_data = fetch_news_data()

        cars_page_widget = setup_cars_page(self.ui, car_data)
        self.ui.set_cars_page(cars_page_widget)
        self.ui.currency_selector.currentTextChanged.connect(self.ui.change_currency)

        news_page_widget = setup_news_page(self.ui, news_data)
        self.ui.set_news_page(news_page_widget)

        comparison_page_widget = setup_comparison_page(self.ui, car_data)
        self.ui.set_comparison_page(comparison_page_widget)

        setup_home_page(
            self.ui,
            car_data,
            news_data,
            on_car_click=lambda car: show_car_details(car, self.ui),
            on_news_click=lambda news: show_news_details(news, self.ui)
        )

        setup_help_page(self.ui)
        setup_about_page(self.ui)

        self.show()

    def connect_signals(self):
        self.ui.menuBtn.clicked.connect(self.ui.leftMenu.toggle)
        self.ui.showUserFormBtn.clicked.connect(self.ui.rightMenu.toggle)

        button_page_map = {
            self.ui.homeBtn: 0,
            self.ui.carsBtn: 1,
            self.ui.compareBtn: 2,
            self.ui.newsBtn: 3,
            self.ui.databaseBtn: 4,
            self.ui.settingsBtn: 5,
            self.ui.helpBtn: 6,
            self.ui.aboutBtn: 7,
        }
        for button, page_index in button_page_map.items():
            button.clicked.connect(lambda checked=False, idx=page_index: self.goto_page(idx))

    def goto_page(self, index):
        self.ui.mainPages.slide_to_index(index)
        buttons = [
            self.ui.homeBtn, self.ui.carsBtn, self.ui.compareBtn,
            self.ui.newsBtn, self.ui.databaseBtn, self.ui.settingsBtn,
            self.ui.helpBtn, self.ui.aboutBtn
        ]
        if 0 <= index < len(buttons):
            self.ui.nav_button_group.set_active(buttons[index])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())