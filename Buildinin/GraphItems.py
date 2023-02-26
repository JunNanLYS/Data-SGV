import sys
from collections import defaultdict

# Builtin
from DataStructureGraphicsView.Functions.polarAngle import polar_angle_x, polar_angle_y
from math import sin, cos

import PySide6
from PySide6 import QtWidgets
from PySide6.QtCore import QPointF, Qt, QTimeLine, QRectF, QSizeF, QLineF, QTime, QCoreApplication, QEventLoop, \
    QPropertyAnimation, QObject, QPoint, Property
from PySide6.QtGui import QBrush, QColor, QPainterPath, QPen, QPolygonF
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItemAnimation, QGraphicsPolygonItem, \
    QGraphicsItem, QStyleOptionGraphicsItem, QWidget, QGraphicsPathItem


def stopTime(second: int):
    endTime = QTime.currentTime().addSecs(second)
    while QTime.currentTime() < endTime:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)


# 图节点
class GraphEllipseItem(QGraphicsEllipseItem):
    __regBrush = QBrush(QColor(58, 143, 192))  # item默认颜色
    __mouse = Qt.MouseButton.NoButton  # 记录鼠标事件

    def __init__(self, x=0, y=0, w=30, h=30, parent=None, name=""):
        super(GraphEllipseItem, self).__init__(x, y, w, h, parent)
        # 初始化
        self.name = name
        self.line = defaultdict(GraphArrowLine)  # k=item: v=line
        self.next = []  # [item1, item2, item3]
        self.moveLine = []  # 所有需要移动的线
        self.select = False  # 用来判断节点是否被选中

        # 设置Setting
        self.setAcceptDrops(True)
        self.setFlags(self.GraphicsItemFlag.ItemIsMovable)  # 可拖动 | 聚焦
        self.setBrush(self.__regBrush)  # 设置节点颜色
        self.setPen(Qt.NoPen)  # 关闭节点边缘线

        # 动画Animation
        self.animation = QGraphicsItemAnimation()
        self.timeLine = QTimeLine(700)  # 动画总时长
        self.animation.setItem(self)
        self.animation.setTimeLine(self.timeLine)

    def mousePressEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.__mouse = event.button()  # 记录事件按键
        self.press_animation()

    def mouseMoveEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        x, y = event.pos().x(), event.pos().y()
        if self.__mouse == Qt.MouseButton.LeftButton:
            r = self.boundingRect().center().x()
            self.moveBy(x - r, y - r)  # 跟随鼠标移动位置
            for line in self.moveLine:
                line.change()
        self.setAcceptDrops(False)

    def mouseReleaseEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.__mouse = Qt.MouseButton.NoButton
        self.setAcceptDrops(True)
        QGraphicsItem.mouseReleaseEvent(self, event)
        self.release_animation()

    # 取消选择改变颜色
    def unselect(self):
        self.setBrush(self.__regBrush)  # 颜色改回默认

    def select_color(self):
        self.setBrush(QBrush(QColor(255, 0, 0)))

    # -------------------------------------------------------------
    # 创建节点动画
    def creat_animation(self):
        self.animation.setScaleAt(0, 1.25, 1.25)
        self.animation.setScaleAt(0.25, 1.0, 1.0)
        self.animation.setScaleAt(0.5, 0.88, 0.88)
        self.animation.setScaleAt(1, 1.0, 1.0)
        self.animation.timeLine().start()

    # 选择动画 | 遍历动画
    def select_animation(self):
        self.animation.setScaleAt(0, 0.8, 0.8)
        self.animation.setScaleAt(0.5, 0.75, 0.75)
        self.animation.setScaleAt(1, 1.0, 1.0)
        self.animation.timeLine().start()
        stopTime(1)

    # 删除动画
    def delete_animation(self):
        self.animation.setScaleAt(0, 0.93, 0.93)
        self.animation.setScaleAt(0.5, 0.63, 0.63)
        self.animation.setScaleAt(0.75, 0.4, 0.4)
        self.animation.setScaleAt(1, 0, 0)
        self.animation.timeLine().start()

    # 点击动画
    def press_animation(self):
        self.animation.setScaleAt(0, 1.0, 1.0)
        self.animation.setScaleAt(1, 0.8, 0.8)
        self.animation.timeLine().start()

    # 释放动画
    def release_animation(self):
        self.animation.setScaleAt(0, 0.8, 0.8)
        self.animation.setScaleAt(1, 1.0, 1.0)
        self.animation.timeLine().start()
    # -------------------------------------------------------------


# 有向
class GraphArrowLine(QGraphicsPathItem, QObject):
    def __init__(self, startItem: QGraphicsItem, endItem: QGraphicsItem):
        super().__init__()
        super(QObject, self).__init__()
        self.start = startItem.pos()  # 起点
        self.end = endItem.pos()  # 终点
        self.startI = startItem
        self.endI = endItem
        self._color = QColor(255, 255, 255)

        # 设置Setting
        self.setPen(QPen(Qt.blue, 2.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))  # 颜色 | 大小
        self.change()  # 取最短路径
        self.create_path()

    # 绘制item
    def create_path(self):
        arrow_size = 10  # 箭头长度
        path = QPainterPath()  # 创建路径

        # 用来连接节点的线
        line = QLineF(self.end, self.start)
        path.moveTo(line.p1())
        path.lineTo(line.p2())
        angle = line.angle()

        # 箭头
        line2 = QLineF(line.p1(), line.p1() + QPointF(-arrow_size, arrow_size))
        line2.setAngle(angle - 35)  # 跟随line1的角度变化
        path.moveTo(line2.p1())
        path.lineTo(line2.p2())

        # 箭头
        line3 = QLineF(line.p1(), line.p1() + QPointF(arrow_size, arrow_size))
        line3.setAngle(angle + 35)  # 跟随line1的角度变化
        path.moveTo(line3.p1())
        path.lineTo(line3.p2())

        path.setFillRule(Qt.WindingFill)
        self.setPath(path)

    # 更新线坐标
    def change(self):
        startI = self.startI
        endI = self.endI
        # 改变节点大小以后要更新
        angleTemp = QLineF(startI.pos() + QPointF(15, 15), endI.pos() + QPointF(15, 15)).angle()  # 获得起点到终点最短路径角度

        angle1, angle2 = -angleTemp, -(angleTemp + 180)  # 极角
        r = 15  # 半径
        x1, y1, x2, y2 = startI.pos().x() + r, startI.pos().y() + r, endI.pos().x() + r, endI.pos().y() + r  # 圆心
        self.start = QPointF(polar_angle_x(x1, r, angle1), polar_angle_y(y1, r, angle1))
        self.end = QPointF(polar_angle_x(x2, r, angle2), polar_angle_y(y2, r, angle2))
        self.create_path()

    # # 移动
    # def move(self):
    #     self.change()
    #     self.create_path()

    # 反转箭头
    def reversed(self):
        startLine = self.startI.line
        endLine = self.endI.line
        startLine.pop(self.endI)
        endLine[self.startI] = self

        # 翻转
        self.startI, self.endI = self.endI, self.startI
        self.change()

    # 将指针从节点中删除
    def delete(self):
        startI, endI = self.startI, self.endI
        startI.line.pop(endI)
        startI.next.pop(startI.next.index(self))
        startI.moveLine.pop(startI.moveLine.index(self))
        endI.moveLine.pop(endI.moveLine.index(self))

