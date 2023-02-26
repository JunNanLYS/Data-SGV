from typing import Any

import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QCursor, QBrush, QColor, QPen, QFont
from PySide6.QtCore import Qt, QPointF, QTimeLine, QTime, QCoreApplication, QEventLoop, QPoint, Property, \
    QPropertyAnimation, QLineF
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsItemAnimation, QGraphicsTextItem, QGraphicsItem, \
    QGraphicsSimpleTextItem

# 树节点
from DataStructureGraphicsView.Class.MyGraphicsItem import MyEllipseItem, MyLineItem
from DataStructureGraphicsView.Functions.polarAngle import polar_angle_x, polar_angle_y


def stopTime(second: int):
    endTime = QTime.currentTime().addSecs(second)
    while QTime.currentTime() < endTime:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)


class TreeNode(MyEllipseItem):
    selectColor = QColor(255, 0, 0)  # 红色

    def __init__(self, x=0, y=0, w=25, h=25, parent=None, left=None, right=None):
        super(TreeNode, self).__init__(x, y, w, h)
        # 初始化
        self.left = left  # 左孩子
        self.right = right  # 右孩子
        self.parent = parent  # 父节点
        self.cur_layer = 0  # 当前层
        self.max_layer = 0  # 最大层
        self.curScene = None  # item所在的scene

        # 当前节点的线
        self.p_line = None
        self.l_line = None
        self.r_line = None

        # 动画Animation
        self.animation = QGraphicsItemAnimation()
        self.timeLine = QTimeLine(800)  # 动画总时长
        self.animation.setItem(self)
        self.animation.setTimeLine(self.timeLine)

    def delete_animation(self):
        self.animation.setScaleAt(0, 1.0, 1.0)
        self.animation.setScaleAt(1, 0.0, 0.0)
        self.animation.timeLine().start()

        stopTime(1)

    def lock_animation(self):
        """
        当节点被锁定时启用该动画
        """
        self.animation.setScaleAt(0.5, 1.15, 1.15)
        self.animation.setScaleAt(0.8, 1.04, 1.04)
        self.animation.setScaleAt(1, 1.0, 1.0)
        self.animation.timeLine().start()

    def set_color(self, state: str):
        if state == 'select':
            self.setBrush(self.selectColor)
            self.setPen(Qt.NoPen)
        elif state == 'lock':
            self.setBrush(Qt.green)
            self.setPen(QPen(Qt.red, 3))
        elif state == 'unselect':
            self.setBrush(self.defaultBrush)
            self.setPen(Qt.NoPen)

    def traversal_animation(self):
        """
        这个方法主要处理TreeView使用Pre,In,Post三种遍历方式
        1. 改变树节点的颜色以表示其已经被遍历到
        2. 启动一个动画来强化效果
        """
        self.setBrush(QBrush(self.selectColor))  # 红色
        # 启动动画
        self.animation.setScaleAt(0.5, 0.8, 0.8)
        self.animation.setScaleAt(0.8, 0.9, 0.9)
        self.animation.setScaleAt(1, 1.0, 1.0)
        self.animation.timeLine().start()

        stopTime(1)

    def itemChange(self, change: PySide6.QtWidgets.QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change == self.GraphicsItemChange.ItemPositionChange:
            ...
        if change == self.GraphicsItemChange.ItemPositionHasChanged:
            if self.l_line:
                self.l_line.change()
            if self.r_line:
                self.r_line.change()
            if self.p_line:
                self.p_line.change()
        return QGraphicsItem.itemChange(self, change, value)

    # 取二叉树最大深度
    def maxDepth(self):
        def dfs(node: TreeNode) -> int:
            if node is None: return 0
            cnt = 1 + max(dfs(node.left), dfs(node.right))
            return cnt

        return dfs(self) - 1

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


class SearchTreeNode(TreeNode):
    def __init__(self, val: str, x=0, y=0, w=30, h=30, parent=None, left=None, right=None):
        super(SearchTreeNode, self).__init__(x, y, w, h)
        # 初始化
        self.val = QGraphicsSimpleTextItem(val)  # 节点值

        # 设置
        self.setFlag(self.GraphicsItemFlag.ItemSendsGeometryChanges)  # 响应改变
        font = QFont()
        font.setPointSize(7)
        font.setBold(True)
        self.val.setFont(font)  # 字体
        self.val.setBrush(QBrush(Qt.black))  # 颜色

    def itemChange(self, change: PySide6.QtWidgets.QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        # 移动前
        if change == self.GraphicsItemChange.ItemPositionChange:
            r = self.boundingRect().center().x()
            w = self.val.boundingRect().center().x()
            h = self.val.boundingRect().center().y()
            self.val.setPos(value.x() + r - w, value.y() + r - h)
        # 移动后
        elif change == self.GraphicsItemChange.ItemPositionHasChanged:
            if self.l_line:
                self.l_line.change()
            if self.r_line:
                self.r_line.change()
            if self.p_line:
                self.p_line.change()
        return QGraphicsItem.itemChange(self, change, value)

    def move_animation(self, end: QPointF):
        """
        接收一个参数 end
        实现节点从一个点移动到另一个点的动画
        """
        animation = QGraphicsItemAnimation()
        timeLine = QTimeLine(500)  # 动画总时长
        animation.setItem(self)
        animation.setTimeLine(timeLine)
        animation.setPosAt(0, self.pos())
        animation.setPosAt(1, end)
        animation.timeLine().start()
        stopTime(1)

    def set_color(self, state: str):
        """
        传入状态，根据状态改变节点当前的外观
        """
        # 路径颜色
        if state == 'path':
            self.setBrush(Qt.white)
            self.setPen(QPen(Qt.red, 3))
        # 选中颜色
        elif state == 'select' or state == 'traversal':
            self.setBrush(Qt.red)
            self.setPen(QPen(Qt.NoPen))
        elif state == 'default':
            self.setBrush(self.defaultBrush)
            self.setPen(QPen(Qt.NoPen))

    def path_animation(self):
        self.set_color('path')
        stopTime(1)


# 树的连接线
class TreeLine(MyLineItem):
    def __init__(self, startItem: TreeNode, endItem: TreeNode, parent=None):
        super(TreeLine, self).__init__(startItem.pos(), endItem.pos(), parent)
        # 设置Setting
        self.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        # 初始化
        self.startI = startItem  # 父节点
        self.endI = endItem  # 孩子节点
        self.startP = startItem.pos()  # 父节点坐标(position)
        self.endP = endItem.pos()  # 孩子节点坐标(position)
        self.curScene = None  # item所在的scene
        self.change()

    # 更新线条
    def change(self):
        """
        使用极角公式，来计算线条两个端点的坐标
        """
        startI = self.startI
        endI = self.endI
        # 改变节点大小以后要更新
        r = self.startI.boundingRect().center().x()
        angleTemp = QLineF(startI.pos() + QPointF(r, r), endI.pos() + QPointF(r, r)).angle()  # 获得起点到终点最短路径角度

        angle1, angle2 = -angleTemp, -(angleTemp + 180)  # 极角
        x1, y1, x2, y2 = startI.pos().x() + r, startI.pos().y() + r, endI.pos().x() + r, endI.pos().y() + r  # 圆心
        self.startP = QPointF(polar_angle_x(x1, r, angle1), polar_angle_y(y1, r, angle1))
        self.endP = QPointF(polar_angle_x(x2, r, angle2), polar_angle_y(y2, r, angle2))

        line = QLineF(self.startP, self.endP)
        self.setLine(line)

    def traversal(self):
        self.setPen(QPen(Qt.red, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        stopTime(1)

    def set_color(self, state: str):
        if state == "default":
            self.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        elif state == "traversal":
            self.setPen(QPen(Qt.red, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        elif state == "path":
            self.setPen(QPen(Qt.red, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        else:
            raise TypeError(f"not have {state}")
