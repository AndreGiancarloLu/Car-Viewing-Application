from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLabel
from PySide6.QtCore import Signal
import json

class FilterBar(QWidget):
    filterChanged = Signal(str, str)  # condition, brand

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        self.condition_text = QLabel("Condition:")
        self.condition_text.setStyleSheet("color: white; font-size: 20px;")
        layout.addWidget(self.condition_text)

        self.condition_dropdown = QComboBox()
        self.condition_dropdown.addItems(["New", "Used", "Both"])
        self.condition_dropdown.setCurrentText("Both")
        self.condition_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #1E293B;
                color: white;
                border-radius: 6px;
                padding: 6px;
                font-size: 16px;
            }
            QComboBox:hover { background-color: #334155; }
            QComboBox QAbstractItemView {
                background-color: #1E293B;
                color: white;
                selection-background-color: #2b6cb0;
                selection-color: white;
                border: 1px solid #334155;
            }
        """)
        self.condition_dropdown.setFixedWidth(140)
        self.condition_dropdown.currentTextChanged.connect(self.emit_filter_changed)
        layout.addWidget(self.condition_dropdown)

        # Spacing between condition and brand
        layout.addSpacing(20)

        self.brand_text = QLabel("Brand:")
        self.brand_text.setStyleSheet("color: white; font-size: 20px;")
        layout.addWidget(self.brand_text)

        brands = json.load(open("data/raw/brands.json", "r"))
        self.brand_dropdown = QComboBox()
        self.brand_dropdown.addItem("All")
        self.brand_dropdown.addItems(brands)
        self.brand_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #1E293B;
                color: white;
                border-radius: 6px;
                padding: 6px;
                font-size: 16px;
            }
            QComboBox:hover { background-color: #334155; }
            QComboBox QAbstractItemView {
                background-color: #1E293B;
                color: white;
                selection-background-color: #2b6cb0;
                selection-color: white;
                border: 1px solid #334155;
            }
        """)
        self.brand_dropdown.setFixedWidth(140)
        self.brand_dropdown.currentTextChanged.connect(self.emit_filter_changed)
        layout.addWidget(self.brand_dropdown)

        # Push everything to the left
        layout.addStretch()

    def emit_filter_changed(self):
        condition = self.condition_dropdown.currentText()
        brand = self.brand_dropdown.currentText()
        self.filterChanged.emit(condition, brand)