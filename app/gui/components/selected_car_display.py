from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPixmap
import weakref
from app.settings.app_settings import app_settings
from app.gui.components.car_widgets import ImageBytesLoader, _CAR_IMAGE_POOL


class SelectedCarDisplay(QWidget):
    change_requested = Signal()

    def __init__(self, car_data=None):
        super().__init__()
        self.car_data = car_data
        self.current_loader = None
        self.image_cache = {}
        self.setup_ui()

        if car_data:
            self.update_car(car_data)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        self.car_image = QLabel("No car selected")
        self.car_image.setAlignment(Qt.AlignCenter)
        self.car_image.setFixedHeight(100)
        self.car_image.setStyleSheet("background-color: #374151; border-radius: 8px; padding: 10px;")
        layout.addWidget(self.car_image)

        self.car_name = QLabel("No car selected")
        self.car_name.setAlignment(Qt.AlignCenter)
        self.car_name.setWordWrap(True)
        self.car_name.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
            margin-top: 3px;
        """)
        layout.addWidget(self.car_name)

        self.car_price = QLabel("")
        self.car_price.setAlignment(Qt.AlignCenter)
        self.car_price.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #00d084;
            margin-bottom: 3px;
        """)
        layout.addWidget(self.car_price)

        selected_layout = QHBoxLayout()
        selected_icon = QLabel("✓")
        selected_icon.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981;")
        selected_text = QLabel("Selected for Comparison")
        selected_text.setStyleSheet("font-size: 16px; color: #10b981; font-weight: 600;")
        selected_layout.addStretch()
        selected_layout.addWidget(selected_icon)
        selected_layout.addWidget(selected_text)
        selected_layout.addStretch()

        selected_widget = QWidget()
        selected_widget.setLayout(selected_layout)
        layout.addWidget(selected_widget)

        self.change_button = QPushButton("Change Selection")
        self.change_button.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 4px;
                padding: 6px;
                font-weight: 600;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        self.change_button.clicked.connect(self.change_requested.emit)
        layout.addWidget(self.change_button)
        layout.addStretch()

        self.setObjectName("SelectedCarDisplay")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #SelectedCarDisplay {
                background-color: #334155;
                border: 2px solid #10b981;
                border-radius: 12px;
                padding: 10px;
            }
        """)

    def update_car(self, car_data):
        self.car_data = car_data
        self.car_name.setText(car_data['title'])

        price = car_data.get("price")
        if price is None:
            formatted_price = "PRICE ON REQUEST"
        else:
            formatted_price = app_settings.format_price(price)
        self.car_price.setText(formatted_price)

        self.load_image_async()

    def load_image_async(self):
        if not self.car_data:
            return

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
            print(f"[SelectedCarDisplay] Failed to build pixmap: {e}")
            self.set_image_failed()

    def set_image(self, pixmap):
        self.car_image.setPixmap(pixmap.scaled(200, 100, Qt.KeepAspectRatio))

    def set_image_failed(self):
        self.car_image.setText("Image not available")