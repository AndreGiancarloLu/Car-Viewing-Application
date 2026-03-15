from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject, Slot, Qt, QTimer
from PySide6.QtGui import QPixmap
import requests
import weakref

_NEWS_IMAGE_POOL = QThreadPool()
_NEWS_IMAGE_POOL.setMaxThreadCount(4)


class NewsBox(QWidget):
    def __init__(self, news_data, on_click, image_cache=None, index=0):
        super().__init__()

        self.news_data = news_data
        self.on_click = on_click
        self.image_cache = image_cache or {}
        self.current_loader = None

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.image_label = QLabel("Loading image...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(150)
        layout.addWidget(self.image_label)

        title = QLabel(news_data.get("title", "Untitled"))
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 600;
            color: #ffffff;
        """)
        layout.addWidget(title)

        date_str = news_data.get("date")
        if date_str:
            date_label = QLabel(date_str)
            date_label.setAlignment(Qt.AlignCenter)
            date_label.setStyleSheet("""
                font-size: 18px;
                color: #cbd5e1;
            """)
            layout.addWidget(date_label)

        button = QPushButton("Read More")
        button.clicked.connect(lambda _, d=news_data: self.on_click(d))
        button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #3b82f6;
            }
        """)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setObjectName("NewsBox")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #NewsBox {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMaximumWidth(500)

        # Staggered start so not all fire at once
        self.delay_timer = QTimer(self)
        self.delay_timer.setSingleShot(True)
        self.delay_timer.timeout.connect(self.load_image_async)
        self.delay_timer.start(index * 100)

    def load_image_async(self):
        image_url = self.news_data.get('image_url', '')
        if not image_url:
            self.set_no_image()
            return

        if image_url in self.image_cache:
            pixmap = self.image_cache[image_url]
            if pixmap and not pixmap.isNull():
                self.set_image(pixmap)
            else:
                self.set_no_image()
            return

        if self.current_loader and (loader := self.current_loader()):
            loader.cancel()

        loader = ImageBytesLoader(image_url)
        loader.signals.finished.connect(self.on_bytes_loaded)
        loader.signals.failed.connect(self.set_no_image)
        self.current_loader = weakref.ref(loader)
        _NEWS_IMAGE_POOL.start(loader)

    @Slot(str, bytes)
    def on_bytes_loaded(self, image_url, data):
        """Called on main thread via signal — safe to create QPixmap here."""
        try:
            pixmap = QPixmap()
            if not pixmap.loadFromData(data):
                self.set_no_image()
                return
            if pixmap.isNull() or pixmap.width() <= 0:
                self.set_no_image()
                return
            self.image_cache[image_url] = pixmap
            self.set_image(pixmap)
        except Exception as e:
            print(f"[NewsBox] Failed to build pixmap: {e}")
            self.set_no_image()

    def set_image(self, pixmap):
        scaled = pixmap.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        if not scaled.isNull():
            self.image_label.setPixmap(scaled)
            self.image_label.setText("")
        else:
            self.set_no_image()

    def set_no_image(self):
        self.image_label.setText("No Image")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("color: gray; font-style: italic;")

    def deleteLater(self):
        if self.delay_timer.isActive():
            self.delay_timer.stop()
        if self.current_loader and (loader := self.current_loader()):
            loader.cancel()
        super().deleteLater()


class ImageBytesLoader(QRunnable):
    """Fetches raw image bytes on a background thread.
    QPixmap is NOT created here — only bytes are transferred via signal.
    The receiving slot (on_bytes_loaded) creates the QPixmap on the main thread."""

    class Signals(QObject):
        finished = Signal(str, bytes)
        failed = Signal()

    def __init__(self, image_url):
        super().__init__()
        self.image_url = image_url
        self.signals = self.Signals()
        self.cancelled = False
        self.setAutoDelete(True)

    @Slot()
    def run(self):
        try:
            if self.cancelled:
                return

            if self.image_url.startswith("http"):
                response = requests.get(self.image_url, timeout=8)
                if self.cancelled:
                    return
                response.raise_for_status()
                data = response.content
            else:
                with open(self.image_url, 'rb') as f:
                    data = f.read()

            if self.cancelled:
                return

            if not data:
                raise ValueError("Empty response")

            self.signals.finished.emit(self.image_url, data)

        except Exception as e:
            print(f"[ImageBytesLoader] Failed: {self.image_url} - {e}")
            if not self.cancelled:
                self.signals.failed.emit()

    def cancel(self):
        self.cancelled = True