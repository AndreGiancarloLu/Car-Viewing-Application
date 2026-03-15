from PySide6.QtCore import QMetaObject, QSize, Qt
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel,
    QLineEdit, QComboBox, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem
)
import app.gui.resources
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import QTableView
from app.gui.components.custom_widgets import SlideMenu, AnimatedStackedWidget, ButtonGroup
#, StyleLoader

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QEasingCurve)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QComboBox, QStyleFactory)
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import QTableView
from pathlib import Path
from app.settings.app_settings import app_settings

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1113, 740)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(True)
        MainWindow.setFont(font)
        MainWindow.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        MainWindow.setStyleSheet(u"* {\n"
        "    border: none;\n"
        "    background: transparent;\n"
        "    padding: 0;\n"
        "    margin: 0;\n"
        "    font-family: \"Segoe UI\", sans-serif;\n"
        "    color: #E2E8F0;\n"
        "}\n"
        "\n"
        "#leftMenu {\n"
        "    background-color: #2B6CB0;\n"
        "}\n"
        "\n"
        "QPushButton {\n"
        "    color: #F7FAFC;\n"
        "    padding: 10px 14px;\n"
        "    border-radius: 8px;\n"
        "    text-align: left;\n"
        "	background-color: #4A5568;\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "    background-color: #3B82C4;\n"
        "}\n"
        "\n"
        "/* Active button style */\n"
        "#homeBtn {\n"
        "    background-color: #1A365D;\n"
        "    border-left: 4px solid #E6F0FA;\n"
        "    font-weight: bold;\n"
        "}\n"
        "\n"
        "/* Main Content Background */\n"
        "#mainBody {\n"
        "    background-color: #1A202C; \n"
        "}\n"
        "\n"
        "/* Header */\n"
        "#header {\n"
        "    background-color: #2D3748;\n"
        "    padding: 10px;\n"
        "}\n"
        "\n"
        "/* Add User Panel */\n"
        "#rightMenu {\n"
        "    background-color: #2B6CB0;\n"
        "    border-radius: 10px;\n"
        "    padding: 10px;\n"
        "}\n"
        "\n"
        "/* Inputs */\n"
        "QLineEdit {\n"
        "    background"
                                "-color: #FFFFFF;\n"
        "    padding: 6px 10px;\n"
        "    border-radius: 5px;\n"
        "    border: 1px solid #CBD5E0;\n"
        "    color: #2D3748;\n"
        "}\n"
        "\n"
        "/* Add User Button */\n"
        "#addUserBtn {\n"
        "    background-color: #4A5568;\n"
        "    color: white;\n"
        "    border-radius: 8px;\n"
        "    padding: 6px 12px;\n"
        "}\n"
        "\n"
        "#addUserBtn:hover {\n"
        "    background-color: #1A365D;\n"
        "}\n"
        "")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QWidget(self.centralwidget)
        self.header.setObjectName(u"header")
        self.horizontalLayout = QHBoxLayout(self.header)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.header)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.menuBtn = QPushButton(self.frame_2)
        self.menuBtn.setObjectName(u"menuBtn")
        self.menuBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(str(Path(__file__).parent / "icons/feather/align-justify.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menuBtn.setIcon(icon)
        self.menuBtn.setIconSize(QSize(24, 24))

        self.horizontalLayout_4.addWidget(self.menuBtn, 0, Qt.AlignmentFlag.AlignLeft)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(16)
        font1.setBold(True)
        self.label.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label)

        self.horizontalLayout.addWidget(self.frame_2, 0, Qt.AlignmentFlag.AlignLeft)

        self.frame = QFrame(self.header)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_4 = QPushButton(self.frame)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(str(Path(__file__).parent / "icons/feather/search.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_4.setIcon(icon1)
        self.pushButton_4.setIconSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(str(Path(__file__).parent / "icons/feather/bell.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(str(Path(__file__).parent /"icons/feather/user.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon3)
        self.pushButton_2.setIconSize(QSize(38, 38))

        self.horizontalLayout_3.addWidget(self.pushButton_2)

        self.horizontalLayout.addWidget(self.frame, 0, Qt.AlignmentFlag.AlignRight)

        self.verticalLayout.addWidget(self.header)
        self.pushButton_2.hide()  # user/profile
        self.pushButton_3.hide()  # bell/notifications  
        self.pushButton_4.hide()  # search

        self.mainBody = QWidget(self.centralwidget)
        self.mainBody.setObjectName(u"mainBody")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainBody.sizePolicy().hasHeightForWidth())
        self.mainBody.setSizePolicy(sizePolicy)
        self.mainBody.setMinimumSize(QSize(1113, 620))
        self.horizontalLayout_2 = QHBoxLayout(self.mainBody)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 9, 0, 0)
        
        self.leftMenu = SlideMenu(self.mainBody)
        self.leftMenu.setObjectName(u"leftMenu")
        self.leftMenu.setMinimumSize(QSize(200, 0))
        self.leftMenu.setMaximumSize(QSize(0, 16777215))
        
        self.verticalLayout_3 = QVBoxLayout(self.leftMenu)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.leftMenu)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(200, 591))
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.widget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.homeBtn = QPushButton(self.frame_3)
        self.homeBtn.setObjectName(u"homeBtn")
        self.homeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(str(Path(__file__).parent /"icons/feather/home.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.homeBtn.setIcon(icon4)

        self.verticalLayout_5.addWidget(self.homeBtn)

        self.carsBtn = QPushButton(self.frame_3)
        self.carsBtn.setObjectName(u"carsBtn")
        self.carsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon5 = QIcon()
        icon5.addFile(str(Path(__file__).parent /"icons/font_awesome/solid/car.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.carsBtn.setIcon(icon5)

        self.verticalLayout_5.addWidget(self.carsBtn)

        self.compareBtn = QPushButton(self.frame_3)
        self.compareBtn.setObjectName(u"compareBtn")
        self.compareBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon6 = QIcon()
        icon6.addFile(str(Path(__file__).parent /"icons/font_awesome/solid/scale-unbalanced.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.compareBtn.setIcon(icon6)

        self.verticalLayout_5.addWidget(self.compareBtn)

        self.newsBtn = QPushButton(self.frame_3)
        self.newsBtn.setObjectName(u"newsBtn")
        self.newsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon7 = QIcon()
        icon7.addFile(str(Path(__file__).parent /"icons/font_awesome/regular/newspaper.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.newsBtn.setIcon(icon7)

        self.verticalLayout_5.addWidget(self.newsBtn)

        self.databaseBtn = QPushButton(self.frame_3)
        self.databaseBtn.setObjectName(u"databaseBtn")
        self.databaseBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon20 = QIcon()
        icon20.addFile(str(Path(__file__).parent /"icons/feather/database.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.databaseBtn.setIcon(icon20)

        self.verticalLayout_5.addWidget(self.databaseBtn)

        self.verticalLayout_4.addWidget(self.frame_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.frame_4 = QFrame(self.widget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.settingsBtn = QPushButton(self.frame_4)
        self.settingsBtn.setObjectName(u"settingsBtn")
        self.settingsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon8 = QIcon()
        icon8.addFile(str(Path(__file__).parent / "icons/feather/settings.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settingsBtn.setIcon(icon8)

        self.verticalLayout_6.addWidget(self.settingsBtn)

        self.helpBtn = QPushButton(self.frame_4)
        self.helpBtn.setObjectName(u"helpBtn")
        self.helpBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon9 = QIcon()
        icon9.addFile(str(Path(__file__).parent /"icons/feather/help-circle.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.helpBtn.setIcon(icon9)

        self.verticalLayout_6.addWidget(self.helpBtn)

        self.aboutBtn = QPushButton(self.frame_4)
        self.aboutBtn.setObjectName(u"aboutBtn")
        self.aboutBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon10 = QIcon()
        icon10.addFile(str(Path(__file__).parent /"icons/feather/info.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.aboutBtn.setIcon(icon10)

        self.verticalLayout_6.addWidget(self.aboutBtn)

        self.verticalLayout_4.addWidget(self.frame_4)

        self.verticalLayout_3.addWidget(self.widget)

        self.horizontalLayout_2.addWidget(self.leftMenu)

        self.mainBodyContent = QWidget(self.mainBody)
        self.mainBodyContent.setObjectName(u"mainBodyContent")
        self.verticalLayout_2 = QVBoxLayout(self.mainBodyContent)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        
        self.mainPages = AnimatedStackedWidget(self.mainBodyContent)
        self.mainPages.setObjectName(u"mainPages")
        
        self.homePage = QWidget()
        self.homePage.setObjectName(u"homePage")
        self.label_8 = QLabel(self.homePage)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(230, 270, 291, 151))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(50)
        self.label_8.setFont(font2)
        self.mainPages.addWidget(self.homePage)
        
        self.carsPage = QWidget()
        self.carsPage.setObjectName(u"carsPage")
        self.mainPages.addWidget(self.carsPage)
        
        self.comparePage = QWidget()
        self.comparePage.setObjectName(u"comparePage")
        self.label_6 = QLabel(self.comparePage)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(290, 270, 291, 151))
        self.label_6.setFont(font2)
        self.mainPages.addWidget(self.comparePage)
        
        self.newsPage = QWidget()
        self.newsPage.setObjectName(u"newsPage")
        self.label_9 = QLabel(self.newsPage)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(380, 250, 291, 151))
        self.label_9.setFont(font2)
        self.mainPages.addWidget(self.newsPage)
        
        self.databasePage = QWidget()
        self.databasePage.setObjectName(u"databasePage")
        self.verticalLayout_10 = QVBoxLayout(self.databasePage)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.widget_3 = QWidget(self.databasePage)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_11 = QVBoxLayout(self.widget_3)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.frame_6 = QFrame(self.widget_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(self.frame_6)
        self.label_4.setObjectName(u"label_4")
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(25)
        self.label_4.setFont(font3)

        self.horizontalLayout_5.addWidget(self.label_4, 0, Qt.AlignmentFlag.AlignLeft)

        self.showUserFormBtn = QPushButton(self.frame_6)
        self.showUserFormBtn.setObjectName(u"showUserFormBtn")
        self.showUserFormBtn.setFont(font)
        self.showUserFormBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon11 = QIcon()
        icon11.addFile(str(Path(__file__).parent /"icons/material_design/add_circle.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.showUserFormBtn.setIcon(icon11)
        self.showUserFormBtn.setIconSize(QSize(24, 24))

        self.horizontalLayout_5.addWidget(self.showUserFormBtn, 0, Qt.AlignmentFlag.AlignRight)

        self.verticalLayout_11.addWidget(self.frame_6)

        self.verticalLayout_10.addWidget(self.widget_3)

        self.mainPages.addWidget(self.databasePage)
        
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName(u"settingsPage")
        settings_layout = QVBoxLayout(self.settingsPage)
        settings_layout.setContentsMargins(50, 50, 50, 50)
        settings_layout.setSpacing(20)

        currency_layout = QHBoxLayout()
        currency_label = QLabel("Select Currency:")
        currency_label.setStyleSheet("color: white; font-size: 16px;")

        self.currency_selector = QComboBox()
        self.currency_selector.addItems(["PHP", "USD", "CNY"])
        self.currency_selector.setStyleSheet("""
            QComboBox {
                background-color: #2c2c2c;
                color: white;
                border: 1px solid #555;
                padding: 5px 10px;
                font-size: 16px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        currency_layout.addWidget(currency_label)
        currency_layout.addWidget(self.currency_selector)
        settings_layout.addLayout(currency_layout)

        self.mainPages.addWidget(self.settingsPage)
        
        self.helpPage = QWidget()
        self.helpPage.setObjectName(u"helpPage")
        self.label_7 = QLabel(self.helpPage)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(340, 270, 291, 151))
        self.label_7.setFont(font2)
        self.mainPages.addWidget(self.helpPage)
        
        self.aboutPage = QWidget()
        self.aboutPage.setObjectName(u"aboutPage")
        self.label_3 = QLabel(self.aboutPage)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(328, 256, 291, 151))
        self.label_3.setFont(font2)
        self.mainPages.addWidget(self.aboutPage)

        self.verticalLayout_2.addWidget(self.mainPages)

        self.horizontalLayout_2.addWidget(self.mainBodyContent)

        self.rightMenu = SlideMenu(self.mainBody)
        self.rightMenu.setObjectName(u"rightMenu")
        self.rightMenu.setMinimumSize(QSize(200, 0))
        
        self.verticalLayout_7 = QVBoxLayout(self.rightMenu)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_2 = QWidget(self.rightMenu)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(164, 262))
        self.verticalLayout_8 = QVBoxLayout(self.widget_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(70, 70))
        self.label_2.setMaximumSize(QSize(70, 70))
        self.label_2.setPixmap(QPixmap(str(Path(__file__).parent /"icons/feather/edit-2.png")))
        self.label_2.setScaledContents(True)

        self.verticalLayout_8.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.frame_5 = QFrame(self.widget_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.username = QLineEdit(self.frame_5)
        self.username.setObjectName(u"username")

        self.verticalLayout_9.addWidget(self.username)

        self.email = QLineEdit(self.frame_5)
        self.email.setObjectName(u"email")

        self.verticalLayout_9.addWidget(self.email)

        self.phoneNumber = QLineEdit(self.frame_5)
        self.phoneNumber.setObjectName(u"phoneNumber")

        self.verticalLayout_9.addWidget(self.phoneNumber)

        self.verticalLayout_8.addWidget(self.frame_5)

        self.addUserBtn = QPushButton(self.widget_2)
        self.addUserBtn.setObjectName(u"addUserBtn")
        self.addUserBtn.setFont(font)
        self.addUserBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon12 = QIcon()
        icon12.addFile(str(Path(__file__).parent /"icons/material_design/add.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addUserBtn.setIcon(icon12)
        self.addUserBtn.setIconSize(QSize(24, 24))

        self.verticalLayout_8.addWidget(self.addUserBtn, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_7.addWidget(self.widget_2, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout_2.addWidget(self.rightMenu)

        self.verticalLayout.addWidget(self.mainBody)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        
        # Setup the custom widgets after UI initialization
        self.setup_custom_widgets()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Car Viewing Application")
        self.label.setText("Car Viewer")
        self.homeBtn.setText("Home")
        self.carsBtn.setText("Cars")
        self.compareBtn.setText("Compare")
        self.newsBtn.setText("News")
        self.databaseBtn.setText("Database")
        self.settingsBtn.setText("Settings")
        self.helpBtn.setText("Help")
        self.aboutBtn.setText("About")
        self.label_8.setText("HOME")
        
        self.label_4.setText("Database")
        self.showUserFormBtn.setText("Add Car")
        self.label_7.setText("HELP")
        self.label_3.setText("ABOUT")
        self.username.setPlaceholderText("Username")
        self.email.setPlaceholderText("Email")
        self.phoneNumber.setPlaceholderText("Phone Number")
        self.addUserBtn.setText("Add User")
    

    def setup_custom_widgets(self):
        """Set up the custom widgets with their configurations."""
        # Setup slide menus
        self.leftMenu.setup(
            default_width=0,  
            expanded_width=200,  
            animation_duration=500,
            easing_curve=QEasingCurve.Type.OutQuad,
            background_color='#2B6CB0'  
        )
        
        # Force the background color using palette
        palette = self.leftMenu.palette()
        palette.setColor(self.leftMenu.backgroundRole(), QColor('#2B6CB0'))
        self.leftMenu.setPalette(palette)
        self.leftMenu.setAutoFillBackground(True)
        
        # Setup right menu
        self.rightMenu.setup(
            default_width=0,  
            expanded_width=200,  
            animation_duration=500,
            easing_curve=QEasingCurve.Type.OutQuad,
            background_color='#2B6CB0'
        )
        
        # Force the right menu background color as well
        palette = self.rightMenu.palette()
        palette.setColor(self.rightMenu.backgroundRole(), QColor('#2B6CB0'))
        self.rightMenu.setPalette(palette)
        self.rightMenu.setAutoFillBackground(True)
        
        # Setup stacked widget animations
        self.mainPages.setup(
            animation_type="slide",
            duration=500,
            easing=QEasingCurve.Type.OutBack,
            direction=Qt.Orientation.Horizontal
        )
        
        # Setup the navigation buttons
        button_page_map = {
            self.homeBtn: 0,  # Home page index
            self.carsBtn: 1,  # Cars page index
            self.compareBtn: 2,  # Compare page index
            self.newsBtn: 3,  # News page index
            self.databaseBtn: 4,  # database page index
            self.settingsBtn: 5,  # Settings page index
            self.helpBtn: 6,  # Help page index
            self.aboutBtn: 7,  # About page index
        }
        self.mainPages.set_navigation(button_page_map)
        
        # Set up the toggle buttons for the sliding menus
        self.menuBtn.clicked.connect(self.leftMenu.toggle)
        self.showUserFormBtn.clicked.connect(self.rightMenu.toggle)
        
        # Set up button icons for left menu toggle
        menu_collapsed_icon = QIcon(str(Path(__file__).parent /"icons/feather/align-justify.png"))
        menu_expanded_icon = QIcon(str(Path(__file__).parent /"icons/feather/chevron-left.png"))  
        self.leftMenu.set_toggle_button(self.menuBtn, menu_collapsed_icon, menu_expanded_icon)
        
        # Set up button icons for right menu toggle
        user_form_collapsed_icon = QIcon(str(Path(__file__).parent /"icons/material_design/add_circle.png"))
        user_form_expanded_icon = QIcon(str(Path(__file__).parent /"icons/feather/window_close.png"))  
        self.rightMenu.set_toggle_button(self.showUserFormBtn, user_form_collapsed_icon, user_form_expanded_icon)
        
        # Create a ButtonGroup for navigation buttons
        nav_buttons = [self.homeBtn, self.carsBtn, self.compareBtn, self.newsBtn, 
                    self.databaseBtn, self.settingsBtn, self.helpBtn, self.aboutBtn]
        
        active_style = """
        background-color: #1A365D;
        border-left: 4px solid #E6F0FA;
        font-weight: bold;
        """
        
        inactive_style = """
        background-color: #4A5568;
        border-left: none;
        font-weight: normal;
        """
        
        self.nav_button_group = ButtonGroup()
        self.nav_button_group.setup(nav_buttons, active_style, inactive_style)
        
        self.nav_button_group.set_active(self.homeBtn)
        self.leftMenu.expand()
        
    
    def setup_database_table_view(self):
        db_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "cars.db"
        db = QSqlDatabase.addDatabase("QSQLITE")

        if db.databaseName() != str(db_path):  
            db.setDatabaseName(str(db_path))

        if not db.open():
            print("[ERROR] Could not open the database.")
            return

        model = QSqlTableModel(parent=None, db=db)
        model.setTable("cars")
        model.select()

        
        table_view = QTableView()
        table_view.setModel(model)

        table_view.setStyleSheet("""
            QTableView {
                background-color: #1A202C;
                alternate-background-color: #2D3748;
                color: #E2E8F0;
                gridline-color: #4A5568;
                border: none;
            }
            
            QHeaderView::section {
                background-color: #2B6CB0;
                color: #FFFFFF;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            
            QTableView::item {
                border-bottom: 1px solid #4A5568;
                padding: 5px;
            }
            
            QTableView::item:selected {
                background-color: #3B82C4;
            }
        """)


        table_view.setSortingEnabled(True)
        table_view.resizeColumnsToContents()
        table_view.setSelectionBehavior(QTableView.SelectRows)
        table_view.setEditTriggers(QTableView.NoEditTriggers)

        self.verticalLayout_10.addWidget(table_view)

    def set_cars_page(self, cars_page):
        self.cars_page = cars_page

    def set_news_page(self, news_page):
        self.news_page = news_page

    def set_comparison_page(self, comparison_page):
        self.comparison_page = comparison_page

    def change_currency(self, currency_code):
        print(f"[DEBUG] Currency changed to: {currency_code}")
        app_settings.selected_currency = currency_code
        print(f"[DEBUG] Currency symbol updated to: {app_settings.currency_symbols[currency_code]}")
        
        app_settings.settingsChanged.emit()
        
        if hasattr(self, "cars_page") and self.cars_page:
            print("[DEBUG] Refreshing all car prices...")
            self.cars_page.refresh_all_prices()
        else:
            print("[DEBUG] No cars_page found to refresh.")