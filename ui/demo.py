from ui.form import Ui_Form
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
import sys


class UiWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)


app = QApplication(sys.argv)

window = UiWindow()
window.show()

sys.exit(app.exec())
