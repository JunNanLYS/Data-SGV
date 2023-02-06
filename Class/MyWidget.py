import PySide6
from PySide6.QtCore import QPointF, Qt
from PySide6 import QtGui
from PySide6.QtWidgets import QWidget


class MyWidget(QWidget):
    mouse = Qt.MouseButton.NoButton  # 记录鼠标
    lastPos = PySide6.QtCore.QPointF()  # 记录鼠标点击的位置
    main_window_pos = PySide6.QtCore.QPointF()

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.mouse = PySide6.QtCore.Qt.MouseButton.NoButton
        self.main_window = self.parent().parent()  # 若Widget在MainWindow下则不为None
        self.item = False  # 当点击空白处时为False
        self.border = False  # 鼠标是否在边框的边上
        # 设置 Setting
        self.setAttribute(Qt.WA_StyledBackground, True)  # 继承绘制
        self.setMouseTracking(True)  # 鼠标拖动

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = event.button()
        self.item = self.childAt(event.pos()) is None
        if event.button() == Qt.MouseButton.LeftButton and self.item:
            self.lastPos = event.globalPos() - self.frameGeometry().topLeft()
            if self.main_window:
                self.main_window_pos = event.globalPos() - self.parent().parent().frameGeometry().topLeft()

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if self.mouse == Qt.MouseButton.LeftButton and self.item:
            if self.main_window:
                main_window = self.parent().parent()
                main_window.move(event.globalPos() - self.main_window_pos)
            else:
                self.move(self.mapToGlobal(event.pos() - self.lastPos))

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = Qt.MouseButton.NoButton
        QWidget.mouseReleaseEvent(self, event)
