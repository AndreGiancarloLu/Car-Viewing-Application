from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGridLayout, QLabel, QStackedWidget
from PySide6.QtCore import Signal, Qt
from app.gui.components.comparison_car_box import ComparisonCarBox
from app.gui.components.selected_car_display import SelectedCarDisplay
class ComparisonCarSelector(QWidget):
    car_selected = Signal(object)
    
    def __init__(self, car_data, side):
        super().__init__()
        self.car_data_all = car_data
        self.side = side  # "left" or "right"
        self.max_cars_per_row = 1  # Just one column for the comparison selector
        self.current_car = None  # Track the selected car
        self.stacked_widget = QStackedWidget()  # To switch between search and selected views
        self.selected_view = None  # Will hold the selected car view
        
        self.page_layout = QVBoxLayout(self)
        
        # Scroll area for car listings
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #1f2937;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #374151;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.container = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        self.container.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.container)
        self.page_layout.addWidget(self.scroll_area)
        self.stacked_widget.addWidget(self.scroll_area)
        self.page_layout.addWidget(self.stacked_widget)
        
        self.setLayout(self.page_layout)
        
        self.display_cars(self.car_data_all)
    
    def display_cars(self, data):
        # Clear existing items
        while self.grid_layout.count() > 0:
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # If no cars match, show a message
        if not data:
            no_cars_label = QLabel("No cars match your search criteria")
            no_cars_label.setStyleSheet("color: white; font-size: 18px;")
            no_cars_label.setAlignment(Qt.AlignCenter)
            self.grid_layout.addWidget(no_cars_label, 0, 0)
            return

        self.car_boxes = []
        for index, car in enumerate(data):
            # One car per row in the comparison selector
            row = index
            col = 0
            def create_selection_handler(car_data):
                return lambda c: self.handle_car_selection(c)
            box = ComparisonCarBox(car, create_selection_handler(car))
            self.car_boxes.append(box)
            self.grid_layout.addWidget(box, row, col)

    def create_selected_view(self):
        if self.selected_view:
            return
            
        self.selected_view = QWidget()
        selected_layout = QVBoxLayout(self.selected_view)
        
        # Create header
        header = QLabel(f"{self.side.capitalize()} Car Selected")
        header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        """)
        
        # Create content showing the selected car
        self.car_display = SelectedCarDisplay(self.current_car)
        self.car_display.change_requested.connect(self.return_to_search)
        
        selected_layout.addWidget(header)
        selected_layout.addWidget(self.car_display)
        selected_layout.addStretch()
        
        # Add to stacked widget
        self.stacked_widget.addWidget(self.selected_view)

    def return_to_search(self):
        self.stacked_widget.setCurrentIndex(0)  # Switch back to search view
        self.current_car = None

    def handle_car_selection(self, car):
        print(f"Car selected: {car['title']}")  # Debug print
        self.current_car = car
        
        # Create selected view if it doesn't exist
        if not self.selected_view:
            self.create_selected_view()
        else:
            # Update the existing selected view
            self.car_display.update_car(car)
        
        # Switch to selected view
        self.stacked_widget.setCurrentIndex(1)
        
        # Emit signal with the selected car
        self.car_selected.emit(car)

    def search_cars(self, query, condition_filter, brand_filter="All"):
        filtered = self.car_data_all
        
        # Apply condition filter
        if condition_filter.lower() != 'both':
            filtered = [car for car in filtered if car.get("condition", "").lower() == condition_filter.lower()]
        
        # Apply brand filter
        if brand_filter.lower() != "all":
            filtered = [car for car in filtered if car.get("brand", "").lower() == brand_filter.lower()]
        
        # Apply search query
        if query:
            terms = query.lower().split()
            filtered = [
                car for car in filtered
                if all(term in car.get("title", "").lower() for term in terms)
            ]
        
        self.display_cars(filtered)