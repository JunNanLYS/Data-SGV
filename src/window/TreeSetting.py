import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

from ui.TreeSetting import Ui_Form
from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect, QGraphicsColorizeEffect, QGraphicsBlurEffect
from src.MyClass.MyWidget import ScrollAreaBackGround, BlackMask


class TreeSettingWidget(ScrollAreaBackGround):
    def __init__(self, parent=None):
        super(TreeSettingWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 阴影
        self.effect = QGraphicsDropShadowEffect()
        self.effect.setColor(Qt.gray)
        self.effect.setOffset(5)
        self.effect.setBlurRadius(3)
        self.setGraphicsEffect(self.effect)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setting = TreeSettingWidget()
    window = BlackMask(setting)
    window.move(0, 0)
    window.resize(setting.width(), setting.height())
    setting.show()
    app.exec()
