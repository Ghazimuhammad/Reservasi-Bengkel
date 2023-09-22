import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget

class ModernComboBox(QComboBox):
    def __init__(self):
        super().__init__()

        # Set stylesheet to customize appearance
        self.setStyleSheet('''
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                background: white;
                selection-background-color: #f0f0f0;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #ccc;
                border-radius: 3px;
            }
            
            QComboBox::down-arrow {
                image: url(down_arrow.png); /* Add path to your custom arrow image */
            }
        ''')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    combo_box = ModernComboBox()
    combo_box.addItem("Option 1")
    combo_box.addItem("Option 2")
    combo_box.addItem("Option 3")
    combo_box.show()
    sys.exit(app.exec_())
