import enum
from math import sin, cos

import PySide6
from typing import Optional

from PySide6.QtCore import QPointF, QLineF, Qt, QRectF, QSize
from PySide6.QtGui import QPen, QPolygonF, QTransform
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsItem, QGraphicsPolygonItem, QGraphicsItemGroup, \
    QGraphicsSimpleTextItem

from ..data_structure import binary_tree, graph

Pi = 3.14159265358979323846264338327950288  # 圆周率


def polar_angle_x(x, r, angle):
    return x + r * cos(angle * Pi / 180)


def polar_angle_y(y, r, angle):
    return y + r * sin(angle * Pi / 180)


class Line(QGraphicsLineItem):

    def __init__(self, item1: Optional[QGraphicsItem], item2: Optional[QGraphicsItem], parent=None):
        super().__init__(item1.pos().x(), item1.pos().y(), item2.pos().x(), item2.pos().y(), parent)
        self.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.item1 = item1
        self.item2 = item2


class LineToEllipse(Line):
    """专用于圆形的直线"""

    def __init__(self, start_item: Optional[QGraphicsItem], end_item: Optional[QGraphicsItem], parent=None):
        super().__init__(start_item, end_item, parent)
        self._start_item: Optional[QGraphicsItem, binary_tree.TreeNode] = start_item
        self._end_item: Optional[QGraphicsItem, binary_tree.TreeNode] = end_item
        self._line_start: Optional[QPointF] = self.start_item.pos()
        self._line_end: Optional[QPointF] = self.end_item.pos()
        self.change()

    def change(self):
        """计算极角坐标，使直线两端最短距离"""
        start_item = self.start_item
        end_item = self.end_item
        # 改变节点大小以后要更新
        r = self.start_item.boundingRect().center().x()
        angle_temp = QLineF(start_item.pos() + QPointF(r, r), end_item.pos() + QPointF(r, r)).angle()  # 获得起点到终点最短路径角度

        angle1, angle2 = -angle_temp, -(angle_temp + 180)  # 极角
        x1, y1, x2, y2 = start_item.pos().x() + r, start_item.pos().y() + r, end_item.pos().x() + r, end_item.pos().y() + r  # 圆心
        self.line_start = QPointF(polar_angle_x(x1, r, angle1), polar_angle_y(y1, r, angle1))
        self.line_end = QPointF(polar_angle_x(x2, r, angle2), polar_angle_y(y2, r, angle2))

        line = QLineF(self.line_start, self.line_end)
        self.setLine(line)

    @property
    def end_item(self):
        return self._end_item

    @end_item.setter
    def end_item(self, new_item):
        self._end_item = new_item
        self.change()

    @property
    def line_start(self):
        return self._line_start

    @line_start.setter
    def line_start(self, pos: QPointF):
        self._line_start = pos
        line = QLineF(self._line_start, self.line_end)
        self.setLine(line)

    @property
    def line_end(self):
        return self._line_end

    @line_end.setter
    def line_end(self, pos: QPointF):
        self._line_end = pos
        line = QLineF(self.line_start, self._line_end)
        self.setLine(line)

    @property
    def start_item(self):
        return self._start_item

    @start_item.setter
    def start_item(self, new_item):
        self._start_item = new_item
        self.change()


# 箭头线
class ArrowLine(QGraphicsItemGroup, Line):
    def __init__(self, start_item: Optional[QGraphicsItem], end_item: Optional[QGraphicsItem], parent=None):
        super().__init__()
        self._start_item: Optional[QGraphicsItem, binary_tree.TreeNode] = start_item
        self._end_item: Optional[QGraphicsItem, binary_tree.TreeNode] = end_item
        self._line_start: Optional[QPointF] = start_item.pos()
        self._line_end: Optional[QPointF] = end_item.pos()

        self.triangle = QPolygonF([QPointF(0, 0), QPointF(-5, 10), QPointF(5, 10)])
        self.triangleItem = QGraphicsPolygonItem(self.triangle)  # 三角形
        self.triangleItem.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))  # 设置三角形笔
        self.triangleItem.setBrush(Qt.black)
        self.line = LineToEllipse(start_item, end_item)  # 直线

        self.addToGroup(self.triangleItem)  # 将三角形添加进group
        self.addToGroup(self.line)  # 将直线添加进group

        self.change()

    def boundingRect(self) -> PySide6.QtCore.QRectF:
        return self.line.boundingRect()

    def change(self):
        """计算极角坐标，使直线两端最短距离"""
        start_item = self.start_item
        end_item = self.end_item
        # 改变节点大小以后要更新
        r = self.start_item.boundingRect().center().x()
        angle_temp = QLineF(start_item.pos() + QPointF(r, r), end_item.pos() + QPointF(r, r)).angle()  # 获得起点到终点最短路径角度

        angle1, angle2 = -angle_temp, -(angle_temp + 180)  # 极角
        x1, y1, x2, y2 = start_item.pos().x() + r, start_item.pos().y() + r, end_item.pos().x() + r, end_item.pos().y() + r  # 圆心
        self.line_start = QPointF(polar_angle_x(x1, r, angle1), polar_angle_y(y1, r, angle1))
        self.line_end = QPointF(polar_angle_x(x2, r, angle2), polar_angle_y(y2, r, angle2))

        line = QLineF(self.line_start, self.line_end)
        self.line.setLine(line)
        angle = self.line.line().angle()
        self.triangleItem.setPos(self.line_end)
        self.triangleItem.setRotation(-angle + 90)

    @property
    def end_item(self):
        return self._end_item

    @end_item.setter
    def end_item(self, new_item):
        self._end_item = new_item
        self.change()

    @property
    def line_start(self):
        return self._line_start

    @line_start.setter
    def line_start(self, pos: QPointF):
        self._line_start = pos
        line = QLineF(self._line_start, self.line_end)
        self.line.setLine(line)

    @property
    def line_end(self):
        return self._line_end

    @line_end.setter
    def line_end(self, pos: QPointF):
        self._line_end = pos
        line = QLineF(self.line_start, self._line_end)
        self.line.setLine(line)

    @property
    def start_item(self):
        return self._start_item

    @start_item.setter
    def start_item(self, new_item):
        self._start_item = new_item
        self.change()


# 带权线
class LineWithWeight(QGraphicsItemGroup, Line):
    weight_text: Optional[QGraphicsSimpleTextItem] = None

    def __init__(self, start_item: Optional[QGraphicsItem], end_item: Optional[QGraphicsItem], weight="权重",
                 parent=None):
        super().__init__()
        self._start_item: Optional[QGraphicsItem, binary_tree.TreeNode] = start_item
        self._end_item: Optional[QGraphicsItem, binary_tree.TreeNode] = end_item
        self._line_start: Optional[QPointF] = self.start_item.pos()
        self._line_end: Optional[QPointF] = self.end_item.pos()

        self.weight = weight
        self.weight_text = QGraphicsSimpleTextItem(self.weight)
        self.line = LineToEllipse(self.start_item, self.end_item)

        self.addToGroup(self.line)
        self.addToGroup(self.weight_text)

        self.weight_text.setPos(self.line.boundingRect().center())
        self.weight_text.setRotation(-self.line.line().angle())

    def boundingRect(self) -> PySide6.QtCore.QRectF:
        return self.line.boundingRect()

    def change(self):
        """计算极角坐标，使直线两端最短距离"""
        start_item = self.start_item
        end_item = self.end_item
        # 改变节点大小以后要更新
        r = self.start_item.boundingRect().center().x()
        angle_temp = QLineF(start_item.pos() + QPointF(r, r), end_item.pos() + QPointF(r, r)).angle()  # 获得起点到终点最短路径角度

        angle1, angle2 = -angle_temp, -(angle_temp + 180)  # 极角
        x1, y1, x2, y2 = start_item.pos().x() + r, start_item.pos().y() + r, end_item.pos().x() + r, end_item.pos().y() + r  # 圆心
        self.line_start = QPointF(polar_angle_x(x1, r, angle1), polar_angle_y(y1, r, angle1))
        self.line_end = QPointF(polar_angle_x(x2, r, angle2), polar_angle_y(y2, r, angle2))

        line = QLineF(self.line_start, self.line_end)
        self.line.setLine(line)
        self.weight_text.setPos(self.line.boundingRect().center())
        self.weight_text.setRotation(-self.line.line().angle())

    @property
    def end_item(self):
        return self._end_item

    @end_item.setter
    def end_item(self, new_item):
        self._end_item = new_item
        self.change()

    @property
    def line_start(self):
        return self._line_start

    @line_start.setter
    def line_start(self, pos: QPointF):
        self._line_start = pos
        line = QLineF(self._line_start, self.line_end)
        self.line.setLine(line)

    @property
    def line_end(self):
        return self._line_end

    @line_end.setter
    def line_end(self, pos: QPointF):
        self._line_end = pos
        line = QLineF(self.line_start, self._line_end)
        self.line.setLine(line)

    @property
    def start_item(self):
        return self._start_item

    @start_item.setter
    def start_item(self, new_item):
        self._start_item = new_item
        self.change()


# 带权箭头线
class ArrowLineWithWeight(ArrowLine):
    weight_text: Optional[QGraphicsSimpleTextItem] = None

    def __init__(self, start_item: Optional[QGraphicsItem], end_item: Optional[QGraphicsItem], weight="权重",
                 parent=None):
        super().__init__(start_item, end_item, parent)
        self.weight = weight
        self.weight_text = QGraphicsSimpleTextItem(self.weight)

        self.addToGroup(self.weight_text)

        self.weight_text.setPos(self.line.boundingRect().center())
        self.weight_text.setRotation(-self.line.line().angle())

    def change(self):
        super().change()
        if self.weight_text:
            self.weight_text.setPos(self.line.boundingRect().center())
            self.weight_text.setRotation(-self.line.line().angle())


class LineEnum(enum.Enum):
    Line = 1
    LineToEllipse = 2
    ArrowLine = 4
    LineWithWeight = 8
    ArrowLineWithWeight = 16

