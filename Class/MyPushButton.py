import PySide6
from PySide6.QtWidgets import QPushButton

class MyPushButton(QPushButton):
    def __init__(self, parent=None):
        super(MyPushButton, self).__init__(parent)
