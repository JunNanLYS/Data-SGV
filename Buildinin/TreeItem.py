import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QCursor, QBrush, QColor, QPen
from PySide6.QtCore import Qt, QPointF, QTimeLine, QTime, QCoreApplication, QEventLoop, QPoint, Property, \
    QPropertyAnimation
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItemAnimation


# 树节点
from BinaryTreeView.Class.MyGraphicsItem import MyEllipseItem, MyLineItem


class TreeNode(MyEllipseItem):
    mouse = Qt.MouseButton.NoButton  # 记录鼠标事件
    selectColor = QColor(255, 0, 0)  # 红色

    def __init__(self, x=0, y=0, w=20, h=20, parent=None, left=None, right=None):
        super(TreeNode, self).__init__(x, y, w, h, parent)
        self.left = left  # 左孩子
        self.right = right  # 右孩子
        self.parent = None  # 父节点

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


# 树的连接线
class TreeLine(MyLineItem):
    ...
