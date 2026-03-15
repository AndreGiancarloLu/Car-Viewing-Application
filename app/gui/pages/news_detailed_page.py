from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QSizePolicy, QScrollArea
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os
import webbrowser


class NewsDetailsPage(QWidget):
    def __init__(self, news_data):
        super().__init__()

        self.setStyleSheet("background: transparent;")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 40)
        main_layout.setSpacing(0)

        # ── Full width title banner ──
        title_banner = QWidget()
        title_banner.setObjectName("TitleBanner")
        title_banner.setAttribute(Qt.WA_StyledBackground, True)
        title_banner.setStyleSheet("""
            #TitleBanner {
                background-color: #1e293b;
                border-bottom: 2px solid #334155;
            }
        """)
        title_banner_layout = QVBoxLayout(title_banner)
        title_banner_layout.setContentsMargins(60, 24, 60, 24)

        title_label = QLabel(news_data.get("title", "Untitled"))
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #f1f5f9;")
        title_banner_layout.addWidget(title_label)

        main_layout.addWidget(title_banner)

        # ── Full width hero image ──
        image_path = news_data.get("local_image_path", "")
        if image_path and os.path.exists(image_path):
            self.image_label = QLabel()
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.setMinimumHeight(200)
            self.image_label.setStyleSheet("background-color: #0f172a;")
            self._image_path = image_path
            # Load pixmap to scale to full width on show
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(700, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled)
            main_layout.addWidget(self.image_label)

        # ── Content area ──
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(60, 32, 60, 32)
        content_layout.setSpacing(28)

        # Meta row
        meta_frame = QFrame()
        meta_frame.setObjectName("MetaFrame")
        meta_frame.setAttribute(Qt.WA_StyledBackground, True)
        meta_frame.setStyleSheet("""
            #MetaFrame {
                background-color: #1e293b;
                border-radius: 10px;
                border-left: 4px solid #2b6cb0;
            }
        """)
        meta_layout = QHBoxLayout(meta_frame)
        meta_layout.setContentsMargins(24, 20, 24, 20)
        meta_layout.setSpacing(60)

        for heading, value in [
            ("Author", news_data.get("author", "Unknown")),
            ("Date", news_data.get("date", "Unknown")),
        ]:
            col = QVBoxLayout()
            col.setSpacing(4)
            h = QLabel(heading.upper())
            h.setStyleSheet("font-size: 12px; color: #64748b; font-weight: bold; letter-spacing: 1px;")
            v = QLabel(value)
            v.setStyleSheet("font-size: 18px; color: #e2e8f0; font-weight: bold;")
            col.addWidget(h)
            col.addWidget(v)
            meta_layout.addLayout(col)

        meta_layout.addStretch()
        content_layout.addWidget(meta_frame)

        # Snippet
        snippet_frame = QFrame()
        snippet_frame.setObjectName("SnippetFrame")
        snippet_frame.setAttribute(Qt.WA_StyledBackground, True)
        snippet_frame.setStyleSheet("""
            #SnippetFrame {
                background-color: #0f172a;
                border-radius: 10px;
                border: 1px solid #334155;
            }
        """)
        snippet_layout = QVBoxLayout(snippet_frame)
        snippet_layout.setContentsMargins(30, 24, 30, 24)
        snippet_layout.setSpacing(12)

        snippet_heading = QLabel("ARTICLE SNIPPET")
        snippet_heading.setStyleSheet("font-size: 12px; color: #64748b; font-weight: bold; letter-spacing: 1px;")
        snippet_layout.addWidget(snippet_heading)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: #334155; min-height: 1px; max-height: 1px;")
        snippet_layout.addWidget(divider)

        snippet_text = news_data.get("intro") or "No snippet available."
        snippet_value = QLabel(snippet_text)
        snippet_value.setWordWrap(True)
        snippet_value.setStyleSheet("font-size: 18px; color: #cbd5e1; line-height: 1.8;")
        snippet_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        snippet_layout.addWidget(snippet_value)

        content_layout.addWidget(snippet_frame)

        # Button
        view_button = QPushButton("View Full Article on AutoDeal.com.ph")
        view_button.setCursor(Qt.PointingHandCursor)
        view_button.setFixedHeight(46)
        view_button.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #10b981; }
        """)
        view_button.clicked.connect(lambda: webbrowser.open(news_data["link"]))
        content_layout.addWidget(view_button, alignment=Qt.AlignLeft)

        content_layout.addStretch()
        main_layout.addWidget(content_widget)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)