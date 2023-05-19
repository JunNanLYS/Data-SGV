import PySide6
from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt

from PySide6.QtGui import QPainter


class RoundedWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(400, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 不显示菜单栏
        self.setAttribute(Qt.WA_TranslucentBackground)  # 不继承背景绘制

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.black)
        painter.drawRoundedRect(self.rect(), 12, 12)


class RoundedWindow(RoundedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        pass

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        pass

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        pass


if __name__ == "__main__":
    import sys

    app = PySide6.QtWidgets.QApplication(sys.argv)
    window = RoundedWidget()
    window.show()
    sys.exit(app.exec())
