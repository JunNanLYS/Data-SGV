import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QCursor, QBrush, QColor, QPen
from PySide6.QtCore import Qt, QPointF, QTimeLine, QTime, QCoreApplication, QEventLoop, QPoint, Property, \
    QPropertyAnimation
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItemAnimation

from BinaryTreeView.Buildinin.TreeItem import TreeNode


class TreeView(QGraphicsView):
    mouse = Qt.MouseButton.NoButton  # 记录鼠标事件

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
        ...

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        ...

    # 鼠标点击后长按移动事件
    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        ...

    # 鼠标释放事件
    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        ...
