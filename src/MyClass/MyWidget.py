import PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QScrollArea, QVBoxLayout, QSlider, QPushButton


class MyWidget(QWidget):
    mouse = Qt.MouseButton.NoButton  # 记录鼠标
    lastPos = PySide6.QtCore.QPointF()  # 记录鼠标点击的位置

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.mouse = PySide6.QtCore.Qt.MouseButton.NoButton
        self.item = False  # 当点击空白处时为False
        self.border = False  # 鼠标是否在边框的边上
        # 设置 Setting
        self.setWindowFlags(Qt.FramelessWindowHint)  # 菜单栏
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景绘制
        self.setAttribute(Qt.WA_StyledBackground, True)  # 继承绘制
        self.setMouseTracking(True)  # 鼠标拖动

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        # print("MyWidget: 鼠标点击")
        self.mouse = event.button()
        self.item = self.childAt(event.pos()) is None
        if event.button() == Qt.MouseButton.LeftButton and self.item:
            self.lastPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if self.mouse == Qt.MouseButton.LeftButton:
            self.move(self.mapToGlobal(event.pos() - self.lastPos))

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = Qt.MouseButton.NoButton
        QWidget.mouseReleaseEvent(self, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(245, 245, 245)))
        painter.drawRoundedRect(self.rect(), 20, 20)


class MyMainWindow(QMainWindow):
    mouse = Qt.MouseButton.NoButton  # 记录鼠标
    lastPos = PySide6.QtCore.QPointF()  # 记录鼠标点击的位置

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.mouse = PySide6.QtCore.Qt.MouseButton.NoButton
        self.item = False  # 当点击空白处时为False
        self.border = False  # 鼠标是否在边框的边上
        # 设置 Setting
        self.setWindowFlags(Qt.FramelessWindowHint)  # 菜单栏
        self.setAttribute(Qt.WA_StyledBackground, True)  # 继承绘制
        self.setMouseTracking(True)  # 鼠标拖动

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = event.button()
        self.item = self.childAt(event.pos()) is None
        if event.button() == Qt.MouseButton.LeftButton and self.item:
            self.lastPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if self.mouse == Qt.MouseButton.LeftButton and self.item:
            self.move(self.mapToGlobal(event.pos() - self.lastPos))

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = Qt.MouseButton.NoButton
        QWidget.mouseReleaseEvent(self, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(245, 245, 245)))
        painter.drawRoundedRect(self.rect(), 30, 30)


class StyleButton(QPushButton):
    def __init__(self, parent=None):
        super(StyleButton, self).__init__(parent)
        self.set_style()

    def set_style(self):
        """用于加载qss"""
        with open("../../qss/StyleButton.qss", "r") as f:
            qss = f.read()
        self.setStyleSheet(qss)


class ScrollAreaBackGround(MyWidget):
    """
    与ScrollArea进行配合，主要功能就是接收子widget鼠标事件并做出反应
    """

    def __init__(self, parent=None):
        super(ScrollAreaBackGround, self).__init__(parent)

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        pass

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        pass


class MyScrollArea(QScrollArea):
    def __init__(self, width=100, high=100, parent=None):
        super(MyScrollArea, self).__init__(parent)
        self.mouse = Qt.MouseButton.NoButton
        # self.resize(width, high)  # 设置大小
        self.scroll_widget = ScrollAreaWidget()
        self.layout = QVBoxLayout(self.scroll_widget)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 垂直滑动条隐藏
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 水平滑动条隐藏

    # 设置样式表
    def set_style_sheet(self):
        with open("../../qss/ScrollArea.qss", "r") as f:
            scroll_area_qss = f.read()
        self.setStyleSheet(scroll_area_qss)


class ScrollAreaWidget(QWidget):
    def __init__(self, parent=None):
        super(ScrollAreaWidget, self).__init__(parent)
        self.mouse = Qt.MouseButton.NoButton

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(245, 245, 245)))
        painter.drawRoundedRect(self.rect(), 0, 0)


class StyleSlider(QSlider):
    def __init__(self, parent=None):
        super(StyleSlider, self).__init__(parent)
        # self.setOrientation(Qt.Horizontal)
        self.set_style()

    def set_style(self):
        with open("../../qss/StyleSlider.qss", "r") as f:
            qss = f.read()
        self.setStyleSheet(qss)


if __name__ == '__main__':
    app = QApplication()
    window = MyWidget()
    window.resize(1000, 800)
    window.show()
    app.exec()
