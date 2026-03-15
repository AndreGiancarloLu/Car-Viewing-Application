import os
import sys

from app.gui.ui_interface import *
from app.gui.components.custom_widgets import SlideMenu, AnimatedStackedWidget, ButtonGroup
from PySide6.QtCore import QEasingCurve, QThreadPool
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
from PySide6.QtSql import QSqlDatabase
from app.etl.etl import run_etl
from app.gui.utils.db_reader import fetch_car_data, fetch_news_data
from app.gui.builders.cars_page_builder import setup_cars_page, show_car_details
from app.gui.builders.news_page_builder import setup_news_page, show_news_details
from app.gui.builders.comparison_page_builder import setup_comparison_page
from app.gui.builders.home_page_builder import setup_home_page
from app.gui.builders.help_page_builder import setup_help_page
from app.gui.builders.about_page_builder import setup_about_page
from app.gui.workers.add_car_worker import AddCarWorker
from app.etl.load import load_cars


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_signals()

        run_etl()
        self.ui.setup_database_table_view()

        self.car_data = fetch_car_data()
        news_data = fetch_news_data()

        cars_page_widget = setup_cars_page(self.ui, self.car_data)
        self.ui.set_cars_page(cars_page_widget)
        self.ui.currency_selector.currentTextChanged.connect(self.ui.change_currency)

        news_page_widget = setup_news_page(self.ui, news_data)
        self.ui.set_news_page(news_page_widget)

        comparison_page_widget = setup_comparison_page(self.ui, self.car_data)
        self.ui.set_comparison_page(comparison_page_widget)

        setup_home_page(
            self.ui,
            self.car_data,
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
        self.ui.addUserBtn.clicked.connect(self.add_car)

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

    def add_car(self):
        url = self.ui.carUrlInput.text().strip()
        if not url:
            self.ui.addCarStatus.setStyleSheet("font-size: 11px; color: #ef4444; padding: 2px 4px;")
            self.ui.addCarStatus.setText("Please enter a URL.")
            return

        self.ui.addUserBtn.setEnabled(False)
        self.ui.addCarStatus.setStyleSheet("font-size: 11px; color: #94a3b8; padding: 2px 4px;")
        self.ui.addCarStatus.setText("Scraping listing...")

        worker = AddCarWorker(url)
        worker.signals.success.connect(self.on_car_added)
        worker.signals.error.connect(self.on_car_add_error)
        QThreadPool.globalInstance().start(worker)

    def on_car_added(self, car):
        # Close Qt's database connection before writing
        if QSqlDatabase.contains("cars_connection"):
            QSqlDatabase.database("cars_connection").close()

        # Write to database
        load_cars([car])

        # Reopen Qt connection for the database page
        self.ui.setup_database_table_view()

        # Refresh cars page
        self.car_data = fetch_car_data()
        self.ui.cars_page.display_cars(self.car_data)

        self.ui.addCarStatus.setStyleSheet("font-size: 11px; color: #34d399; padding: 2px 4px;")
        self.ui.addCarStatus.setText(f"Added: {car['title']}")
        self.ui.carUrlInput.clear()
        self.ui.addUserBtn.setEnabled(True)

    def on_car_add_error(self, error_msg):
        self.ui.addCarStatus.setStyleSheet("font-size: 11px; color: #ef4444; padding: 2px 4px;")
        self.ui.addCarStatus.setText(f"Error: {error_msg}")
        self.ui.addUserBtn.setEnabled(True)

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