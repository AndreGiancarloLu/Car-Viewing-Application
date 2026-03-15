import random
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QScrollArea, QSizePolicy, QFrame)
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QPixmap
from app.gui.components.car_widgets import ImageBytesLoader, _CAR_IMAGE_POOL
from app.gui.components.news_widgets import ImageBytesLoader as NewsImageBytesLoader, _NEWS_IMAGE_POOL
import weakref


class FeaturedCarSlide(QWidget):
    def __init__(self, car_data, on_click):
        super().__init__()
        self.car_data = car_data
        self.on_click = on_click
        self.current_loader = None

        self.setObjectName("FeaturedCarSlide")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("#FeaturedCarSlide { background-color: #0f172a; border-radius: 14px; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedHeight(320)
        self.image_label.setText("Loading...")
        self.image_label.setStyleSheet("""
            background-color: #0f172a;
            border-radius: 14px 14px 0 0;
            color: #475569;
            font-size: 16px;
        """)
        layout.addWidget(self.image_label)

        info_bar = QWidget()
        info_bar.setObjectName("CarInfoBar")
        info_bar.setAttribute(Qt.WA_StyledBackground, True)
        info_bar.setStyleSheet("""
            #CarInfoBar {
                background-color: #1e293b;
                border-radius: 0 0 14px 14px;
                border-top: 1px solid #334155;
            }
        """)
        info_layout = QHBoxLayout(info_bar)
        info_layout.setContentsMargins(20, 14, 20, 14)
        info_layout.setSpacing(12)

        text_col = QVBoxLayout()
        text_col.setSpacing(4)

        name_label = QLabel(car_data.get("title", "Unknown Car"))
        name_label.setStyleSheet("color: #f1f5f9; font-size: 20px; font-weight: bold;")

        brand_label = QLabel(car_data.get("brand", ""))
        brand_label.setStyleSheet("color: #94a3b8; font-size: 15px;")

        text_col.addWidget(name_label)
        text_col.addWidget(brand_label)

        from app.settings.app_settings import app_settings
        price = car_data.get("price")
        price_text = app_settings.format_price(price) if price else "PRICE ON REQUEST"
        price_label = QLabel(price_text)
        price_label.setStyleSheet("color: #34d399; font-size: 18px; font-weight: bold;")

        view_btn = QPushButton("View Car")
        view_btn.setCursor(Qt.PointingHandCursor)
        view_btn.setFixedWidth(130)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #10b981; }
        """)
        view_btn.clicked.connect(lambda: self.on_click(self.car_data))

        info_layout.addLayout(text_col)
        info_layout.addStretch()
        info_layout.addWidget(price_label, 0, Qt.AlignVCenter)
        info_layout.addWidget(view_btn, 0, Qt.AlignVCenter)

        layout.addWidget(info_bar)
        self.load_image()

    def load_image(self):
        image_path = self.car_data.get("local_image_path") or self.car_data.get("image_url", "")
        if not image_path:
            self.image_label.setText("No Image")
            return
        loader = ImageBytesLoader(image_path)
        loader.signals.finished.connect(self.on_bytes_loaded)
        loader.signals.failed.connect(lambda: self.image_label.setText("No Image"))
        self.current_loader = weakref.ref(loader)
        _CAR_IMAGE_POOL.start(loader)

    @Slot(str, bytes)
    def on_bytes_loaded(self, path, data):
        try:
            pixmap = QPixmap()
            if not pixmap.loadFromData(data) or pixmap.isNull():
                self.image_label.setText("No Image")
                return
            scaled = pixmap.scaled(
                self.image_label.width() or 900, 320,
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)
        except Exception as e:
            print(f"[FeaturedCarSlide] pixmap error: {e}")
            self.image_label.setText("No Image")


class NewsCard(QWidget):
    def __init__(self, news_data, on_click):
        super().__init__()
        self.news_data = news_data
        self.on_click = on_click
        self.current_loader = None

        self.setObjectName("NewsCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #NewsCard {
                background-color: #1e293b;
                border-radius: 10px;
                border: 1px solid #334155;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedHeight(120)
        self.image_label.setText("Loading...")
        self.image_label.setStyleSheet("""
            background-color: #0f172a;
            border-radius: 10px 10px 0 0;
            color: #475569;
            font-size: 13px;
        """)
        layout.addWidget(self.image_label)

        text_widget = QWidget()
        text_widget.setStyleSheet("background: transparent;")
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(10, 8, 10, 8)
        text_layout.setSpacing(4)

        title = QLabel(news_data.get("title", "Untitled"))
        title.setWordWrap(True)
        title.setStyleSheet("color: #e2e8f0; font-size: 13px; font-weight: bold;")
        title.setMaximumHeight(52)

        date_label = QLabel(news_data.get("date", ""))
        date_label.setStyleSheet("color: #64748b; font-size: 12px;")

        read_btn = QPushButton("Read More")
        read_btn.setCursor(Qt.PointingHandCursor)
        read_btn.setFixedHeight(28)
        read_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 4px;
                font-size: 12px;
                padding: 2px 6px;
            }
            QPushButton:hover { background-color: #3b82f6; }
        """)
        read_btn.clicked.connect(lambda: self.on_click(self.news_data))

        text_layout.addWidget(title)
        text_layout.addWidget(date_label)
        text_layout.addStretch()
        text_layout.addWidget(read_btn)

        layout.addWidget(text_widget)
        self.load_image()

    def load_image(self):
        image_url = self.news_data.get("image_url", "")
        if not image_url:
            self.image_label.setText("No Image")
            return
        loader = NewsImageBytesLoader(image_url)
        loader.signals.finished.connect(self.on_bytes_loaded)
        loader.signals.failed.connect(lambda: self.image_label.setText("No Image"))
        self.current_loader = weakref.ref(loader)
        _NEWS_IMAGE_POOL.start(loader)

    @Slot(str, bytes)
    def on_bytes_loaded(self, path, data):
        try:
            pixmap = QPixmap()
            if not pixmap.loadFromData(data) or pixmap.isNull():
                self.image_label.setText("No Image")
                return
            scaled = pixmap.scaled(300, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled)
        except Exception as e:
            self.image_label.setText("No Image")


class HeroSlideshow(QWidget):
    def __init__(self, cars, on_click, interval_ms=5000):
        super().__init__()
        self.slides = []
        self.current_index = 0

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(6)

        slide_row = QHBoxLayout()
        slide_row.setContentsMargins(0, 0, 0, 0)
        slide_row.setSpacing(8)

        self.prev_btn = QPushButton("‹")
        self.prev_btn.setFixedSize(44, 44)
        self.prev_btn.setCursor(Qt.PointingHandCursor)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(45,55,72,0.9);
                color: white;
                border-radius: 22px;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2b6cb0; }
        """)
        self.prev_btn.clicked.connect(self.prev_slide)

        self.slide_container = QWidget()
        self.slide_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.slide_inner = QVBoxLayout(self.slide_container)
        self.slide_inner.setContentsMargins(0, 0, 0, 0)

        self.next_btn = QPushButton("›")
        self.next_btn.setFixedSize(44, 44)
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(45,55,72,0.9);
                color: white;
                border-radius: 22px;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2b6cb0; }
        """)
        self.next_btn.clicked.connect(self.next_slide)

        slide_row.addWidget(self.prev_btn, 0, Qt.AlignVCenter)
        slide_row.addWidget(self.slide_container)
        slide_row.addWidget(self.next_btn, 0, Qt.AlignVCenter)
        outer.addLayout(slide_row)

        dots_widget = QWidget()
        dots_layout = QHBoxLayout(dots_widget)
        dots_layout.setAlignment(Qt.AlignCenter)
        dots_layout.setSpacing(8)
        self.dots = []
        for i in range(len(cars)):
            dot = QLabel("●")
            dot.setAlignment(Qt.AlignCenter)
            dot.setStyleSheet("color: #4a5568; font-size: 12px;")
            self.dots.append(dot)
            dots_layout.addWidget(dot)
        outer.addWidget(dots_widget)

        for car in cars:
            slide = FeaturedCarSlide(car, on_click)
            self.slides.append(slide)
            self.slide_inner.addWidget(slide)
            slide.hide()

        self.show_slide(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_slide)
        self.timer.start(interval_ms)

    def show_slide(self, index):
        for i, s in enumerate(self.slides):
            s.setVisible(i == index)
        for i, d in enumerate(self.dots):
            d.setStyleSheet(
                "color: #63b3ed; font-size: 15px;" if i == index
                else "color: #4a5568; font-size: 12px;"
            )
        self.current_index = index

    def next_slide(self):
        self.timer.stop()
        self.show_slide((self.current_index + 1) % len(self.slides))
        self.timer.start()

    def prev_slide(self):
        self.timer.stop()
        self.show_slide((self.current_index - 1) % len(self.slides))
        self.timer.start()


def setup_home_page(ui, car_data, news_data, on_car_click, on_news_click):
    for child in ui.homePage.findChildren(QLabel):
        child.deleteLater()

    root = QVBoxLayout(ui.homePage)
    root.setContentsMargins(20, 20, 20, 20)
    root.setSpacing(20)

    title = QLabel("Welcome to Car Viewer")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 26px; font-weight: bold; color: #e2e8f0;")
    root.addWidget(title)

    cars_heading = QLabel("Featured Cars")
    cars_heading.setStyleSheet("font-size: 18px; font-weight: bold; color: #63b3ed;")
    root.addWidget(cars_heading)

    featured_cars = random.sample(car_data, min(5, len(car_data)))
    hero = HeroSlideshow(featured_cars, on_car_click, interval_ms=5000)
    root.addWidget(hero)

    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("background-color: #334155; min-height: 1px; max-height: 1px;")
    root.addWidget(line)

    news_heading = QLabel("Featured News")
    news_heading.setStyleSheet("font-size: 18px; font-weight: bold; color: #63b3ed;")
    root.addWidget(news_heading)

    featured_news = news_data[:5]
    news_row = QHBoxLayout()
    news_row.setSpacing(12)
    for article in featured_news:
        card = NewsCard(article, on_news_click)
        news_row.addWidget(card)
    root.addLayout(news_row)

    root.addStretch()
    return ui.homePage