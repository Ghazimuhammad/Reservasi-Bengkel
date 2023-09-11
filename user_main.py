from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QScrollArea, QWidget, QFrame, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize, QRect

class UserMain(QMainWindow):
    def __init__(self):
        super(UserMain, self).__init__()

        self.main_page = uic.loadUi('file_ui/user_main_menu.ui', self)

        
        self.set_icon()

        self.create_account = self.findChild(QPushButton, 'push_sparepart')
        self.create_account.clicked.connect(self.to_sparepart)

        self.show()

    def to_sparepart(self):
        self.main_page.close()
        self.sparepart_page = Sparepart()
        self.sparepart_page.show()
    
    def set_icon(self):
        self.label = self.findChild(QLabel, 'logo')
        pixmap = QPixmap('Pictures/image 2.png')
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        self.push_sparepart = self.findChild(QPushButton, 'push_sparepart')
        self.push_sparepart.setIcon(QIcon("Pictures/sparepart.png"))
        self.push_sparepart.setIconSize(QSize(65, 65))

        self.push_reservation = self.findChild(QPushButton, 'push_reservation')
        self.push_reservation.setIcon(QIcon("Pictures/reservation.png"))
        self.push_reservation.setIconSize(QSize(90, 95))

        self.push_service_list = self.findChild(QPushButton, 'push_service_list')
        self.push_service_list.setIcon(QIcon("Pictures/list.png"))
        self.push_service_list.setIconSize(QSize(65, 65))



    
class Sparepart(QMainWindow):
    def __init__(self):
        super(Sparepart, self).__init__()

        self.sparepart_page = uic.loadUi('file_ui/sparepart_menu.ui', self)

        self.label = self.findChild(QLabel, 'logo_sparepart')
        pixmap = QPixmap('Pictures/sparepart.png')
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        self.push_back = self.findChild(QPushButton, 'push_back')
        self.push_back.clicked.connect(self.to_user_main)
        self.insert_sparepart_menu()

        self.show()

    def to_user_main(self):
        self.sparepart_page.close()
        self.user_main = UserMain()
        self.user_main.show()
    
    def insert_sparepart_menu(self):
        scrollable_layout = SparepartMenu()
        self.sparepart_page.verticalLayout.addWidget(scrollable_layout)


class SparepartMenu(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Create a QWidget for the content
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)

        # Create a QGridLayout for the content widget
        content_layout = QGridLayout(content_widget)

        # Create a list to keep track of the counters
        self.counters = []

        # Add widgets to the layout
        for i in range(20):  # Add 20 labels for demonstration
            label = QLabel(f'Label {i+1}')
            content_layout.addWidget(label, i, 0)

            price = QLabel(f'10k')
            content_layout.addWidget(price, i, 1)

            # Create buttons for each label
            button_plus = QPushButton(f'+')
            content_layout.addWidget(button_plus, i, 2)

            self.counters.append(0)  # Initialize counters

            count = QLabel("0")
            content_layout.addWidget(count, i, 3)
            count.setObjectName(f'label_{i}')

            button_minus = QPushButton(f'-')
            content_layout.addWidget(button_minus, i, 4)

            # Connect button signals to functions
            button_plus.clicked.connect(lambda checked, idx=i: self.handle_button_click(idx, 1))
            button_minus.clicked.connect(lambda checked, idx=i: self.handle_button_click(idx, -1))

        # Set the main layout for the window
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def handle_button_click(self, index, increment):
        # This function will be called when any button is clicked
        self.counters[index] += increment
        label = self.findChild(QLabel, f'label_{index}')  # Find the label by its object name
        if label is not None:
            label.setText(str(self.counters[index]))