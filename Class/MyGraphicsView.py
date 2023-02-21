import PySide6
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene


class MyTreeView(QGraphicsView):
    def __init__(self, parent=None):
        super(MyTreeView, self).__init__(parent)

        # 初始化
        self.mouse = Qt.MouseButton.NoButton  # 记录鼠标事件
        self._enlarge = 0  # 放大的次数
        self._shrink = 0  # 缩小的次数
        self.last_pos = QtCore.QPointF()  # 作用 -> 记录鼠标位置，移动view

        # 设置Setting
        self.setScene(QGraphicsScene(self.x(), self.y(), self.width(), self.height(), self))  # 内置一个场景
        self.viewport().setProperty("cursor", QCursor(Qt.CrossCursor))  # 设置光标为十字型  ( + )

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.mouse = event.button()
            self.last_pos = self.mapToScene(event.pos())
            return

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if self.mouse == Qt.MiddleButton:
            dp = self.mapToScene(event.pos()) - self.last_pos
            sRect = self.sceneRect()
            self.setSceneRect(sRect.x() - dp.x(), sRect.y() - dp.y(), sRect.width(), sRect.height())
            self.last_pos = self.mapToScene(event.pos())
            return
        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = Qt.MouseButton.NoButton

    def wheelEvent(self, event) -> None:
        # 等比例缩放
        wheelValue = event.angleDelta().y()
        ratio = wheelValue / 1200 + 1  # ratio -> 1.1 or 0.9
        if ratio > 1:  # 放大次数6
            if self._enlarge < 6:
                self._enlarge += 1
                self._shrink -= 1
                self.scale(ratio, ratio)
        else:  # 缩小次数10
            if self._shrink < 10:
                self._shrink += 1
                self._enlarge -= 1
                self.scale(ratio, ratio)
