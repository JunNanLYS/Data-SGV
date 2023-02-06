import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QCursor, QBrush, QColor, QPen
from PySide6.QtCore import Qt, QPointF, QTimeLine, QTime, QCoreApplication, QEventLoop, QPoint, Property, \
    QPropertyAnimation
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItemAnimation

from BinaryTreeView.Buildinin.TreeItem import TreeNode


class TreeView(QGraphicsView):
    mouse = Qt.MouseButton.NoButton  # 记录鼠标事件
    _enlarge = 0  # 放大的次数
    _shrink = 0  # 缩小的次数

    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)

        # 设置Setting
        self.setScene(QGraphicsScene(self.x(), self.y(), self.width(), self.height(), self))  # 内置一个场景
        self.viewport().setProperty("cursor", QCursor(Qt.CrossCursor))  # 设置光标为十字型  ( + )
        node = TreeNode()
        self.scene().addItem(node)
        node.setPos(0, -300)

    # 鼠标点击事件
    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.MiddleButton:
            ...

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        item = self.scene().itemAt(event.pos())
        # 点击节点
        if item and item == TreeNode:
            # 创建左孩子
            if event.button() == Qt.MouseButton.LeftButton:
                print("hi")
            # 创建右孩子
            elif event.button() == Qt.MouseButton.RightButton:
                ...

    # 鼠标点击后长按移动事件
    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        ...

    # 滚轮
    def wheelEvent(self, event) -> None:
        # 等比例缩放
        wheelValue = event.angleDelta().y()
        ratio = wheelValue / 1200 + 1  # ratio -> 1.1 or 0.9
        if ratio > 1:  # 放大次数6
            if self._enlarge < 6:
                self._enlarge += 1
                self._shrink -= 1
                self.scale(ratio, ratio)
        else:  # 缩小次数5
            if self._shrink < 5:
                self._shrink += 1
                self._enlarge -= 1
                self.scale(ratio, ratio)

    # 鼠标释放事件
    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        ...
