import PySide6
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton

from ui.Setting import Ui_Form
from src.MyClass.MyWidget import ScrollAreaBackGround


class SettingWidget(ScrollAreaBackGround):
    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication()
    widget = SettingWidget()
    widget.show()
    app.exec()
