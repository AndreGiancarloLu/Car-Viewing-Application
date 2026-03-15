from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QThreadPool, Signal, Slot
from PySide6.QtGui import QPixmap
import weakref
from app.settings.app_settings import app_settings
from app.gui.components.car_widgets import ImageBytesLoader, _CAR_IMAGE_POOL


class ComparisonCarBox(QWidget):
    def __init__(self, car_data, on_select):
        super().__init__()
        self.car_data = car_data
        self.on_select = on_select
        self.current_loader = None
        self.image_cache = {}

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.car_image = QLabel("Loading image...")
        self.car_image.setAlignment(Qt.AlignCenter)
        self.car_image.setFixedHeight(120)

        car_name = QLabel(self.car_data['title'])
        car_name.setAlignment(Qt.AlignCenter)
        car_name.setWordWrap(True)
        car_name.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
            padding-bottom: 4px;
        """)

        self.car_price = QLabel()
        self.car_price.setAlignment(Qt.AlignCenter)
        self.car_price.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #00d084;
            padding-top: 4px;
        """)
        self.update_price()

        select_button = QPushButton("Select for Comparison")
        car_data_ref = self.car_data
        select_button.clicked.connect(lambda checked=False, car=car_data_ref: self.on_select(car))
        select_button.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #10b981;
            }
        """)

        layout.addWidget(self.car_image)
        layout.addWidget(car_name)
        layout.addWidget(self.car_price)
        layout.addWidget(select_button)
        self.setLayout(layout)
        self.setObjectName("ComparisonCarBox")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #ComparisonCarBox {
                background-color: #334155;
                border: 1px solid #3c4a5a;
                border-radius: 12px;
                padding: 10px;
            }
        """)

        self.load_image_async()

    def load_image_async(self):
        image_path = self.car_data.get('local_image_path') or self.car_data.get('image_url', '')
        if not image_path:
            self.set_image_failed()
            return

        if image_path in self.image_cache:
            pixmap = self.image_cache[image_path]
            if pixmap and not pixmap.isNull():
                self.set_image(pixmap)
            else:
                self.set_image_failed()
            return

        if self.current_loader and (loader := self.current_loader()):
            loader.cancel()

        loader = ImageBytesLoader(image_path)
        loader.signals.finished.connect(self.on_bytes_loaded)
        loader.signals.failed.connect(self.set_image_failed)
        self.current_loader = weakref.ref(loader)
        _CAR_IMAGE_POOL.start(loader)

    @Slot(str, bytes)
    def on_bytes_loaded(self, image_path, data):
        """Called on main thread via signal — safe to create QPixmap here."""
        try:
            pixmap = QPixmap()
            if not pixmap.loadFromData(data):
                self.set_image_failed()
                return
            if pixmap.isNull() or pixmap.width() <= 0:
                self.set_image_failed()
                return
            self.image_cache[image_path] = pixmap
            self.set_image(pixmap)
        except Exception as e:
            print(f"[ComparisonCarBox] Failed to build pixmap: {e}")
            self.set_image_failed()

    def set_image(self, pixmap):
        self.car_image.setPixmap(pixmap.scaled(200, 120, Qt.KeepAspectRatio))

    def set_image_failed(self):
        self.car_image.setText("Image not available")

    def update_price(self):
        price = self.car_data.get("price")
        if price is None:
            formatted_price = "PRICE ON REQUEST"
        else:
            formatted_price = app_settings.format_price(price)
        self.car_price.setText(formatted_price)