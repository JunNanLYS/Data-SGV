from ui.setting import UiSetting
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from src.widgets.windows import RoundedWindow, RoundedWidget, DefaultWidget
from qfluentwidgets import PushButton
import sys


class UiWindow(DefaultWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = UiSetting()
        self.ui.setupUi(self)
        self.__init_node_color()

        self.new_button = PushButton(self.ui.scroll_area_widget)
        self.new_button2 = PushButton(self.ui.scroll_area_widget)
        self.new_button.setText("button1")
        self.new_button2.setText("button2")
        self.ui.layout_current.addWidget(self.new_button)
        self.ui.layout_current.addWidget(self.new_button2)

    def __init_node_color(self):
        ui = self.ui
        ui.combobox_node_color.addItems(["red", "green", "black", "blue"])



app = QApplication(sys.argv)

window = UiWindow()
window.show()

sys.exit(app.exec())
