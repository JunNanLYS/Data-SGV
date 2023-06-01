import enum
from math import sin, cos
from typing import Union

import PySide6
from PySide6.QtCore import QPointF, QLineF, Qt, QLine
from PySide6.QtGui import QPen, QPolygonF
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsItem, QGraphicsPolygonItem, QGraphicsItemGroup, \
    QGraphicsSimpleTextItem

Pi = 3.14159265358979323846264338327950288  # 圆周率


def polar_angle_x(x, r, angle):
    return x + r * cos(angle * Pi / 180)


def polar_angle_y(y, r, angle):
    return y + r * sin(angle * Pi / 180)


class Line(QGraphicsItemGroup):
    CLASS_NAME = "Line"

    def __init__(self, start_item: QGraphicsItem, end_item: QGraphicsItem, parent: QGraphicsItem = None):
        super().__init__(parent)
        self._start_item = start_item
        self._end_item = end_item
        self._line_start = self._start_item.pos()
        self._line_end = self._end_item.pos()

        self.line_item = QGraphicsLineItem(self._line_start.x(), self._line_start.y(),
                                           self._line_end.x(), self._line_end.y(),
                                           self)
        self.line_item.setPen(QPen(Qt.black, 2.5))
        self.weight = QGraphicsSimpleTextItem(self)
        self.weight.setText("")

        # add to group
        self.addToGroup(self.line_item)

        # change
        self.change()

    def boundingRect(self) -> PySide6.QtCore.QRectF:
        return self.line.boundingRect()

    def change(self):
        start_pos = self._start_item.pos()
        end_pos = self._end_item.pos()
        # 改变节点大小以后要更新
        r = self._start_item.boundingRect().center().x()  # 圆半径
        angle_temp = QLineF(start_pos + QPointF(r, r), end_pos + QPointF(r, r)).angle()  # 获得起点到终点最短路径角度

        angle1, angle2 = -angle_temp, -(angle_temp + 180)  # 极角
        x1, y1, x2, y2 = start_pos.x() + r, start_pos.y() + r, end_pos.x() + r, end_pos.y() + r  # 圆心
        self.line_start = QPointF(polar_angle_x(x1, r, angle1), polar_angle_y(y1, r, angle1))
        self.line_end = QPointF(polar_angle_x(x2, r, angle2), polar_angle_y(y2, r, angle2))
        # self.setLine(QLine(self.line_start.x(), self.line_start.y(), self.line_end.x(), self.line_end.y()))

    def setLine(self, line: Union[QLine, QLineF]):
        self.line.setLine(line)

    @property
    def line(self):
        return self.line_item

    @property
    def line_start(self):
        return self._line_start

    @line_start.setter
    def line_start(self, position: QPointF):
        self._line_start = position
        self.line.setLine(QLineF(self._line_start, self._line_end))

    @property
    def line_end(self):
        return self._line_end

    @line_end.setter
    def line_end(self, position: QPointF):
        self._line_end = position
        self.line.setLine(QLineF(self._line_start, self._line_end))

    @property
    def start_item(self):
        return self._start_item

    @start_item.setter
    def start_item(self, item: QGraphicsItem):
        self._start_item = item
        self.change()

    @property
    def end_item(self):
        return self._end_item

    @end_item.setter
    def end_item(self, item: QGraphicsItem):
        self._end_item = item
        self.change()


class LineWithWeight(Line):
    CLASS_NAME = "LineWithWeight"

    def __init__(self, start_item: QGraphicsItem, end_item: QGraphicsItem, parent: QGraphicsItem = None):
        super().__init__(start_item, end_item, parent)
        self.weight = QGraphicsSimpleTextItem(self)
        self.weight.setText("weight")
        self.weight.setPos(self.boundingRect().center())
        self.weight.setRotation(-self.line.line().angle())

        # add to group
        self.addToGroup(self.weight)

    def change(self):
        super().change()
        if self.weight is not None:
            self.weight.setPos(self.boundingRect().center())
            angle = -self.line.line().angle()
            if -90 >= angle >= -270:
                angle -= 180
                self.weight.setRotation(angle)
            else:
                self.weight.setRotation(angle)

    def set_weight(self, weight: str):
        """set line weight"""
        self.weight.setText(weight)


class ArrowLine(Line):
    CLASS_NAME = "ArrowLine"
    triangleItem = None

    def __init__(self, start_item, end_item, parent=None):
        super().__init__(start_item, end_item, parent)
        # init triangle
        triangle = QPolygonF([QPointF(0, 0), QPointF(-5, 10), QPointF(5, 10)])
        self.triangleItem = QGraphicsPolygonItem(triangle, self)  # 三角形
        self.triangleItem.setPen(QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))  # 设置三角形笔
        self.triangleItem.setBrush(Qt.black)

        angle = self.line.line().angle()
        self.triangleItem.setPos(self.line_end)
        self.triangleItem.setRotation(-angle + 90)

        # add to group
        self.addToGroup(self.triangleItem)

    def change(self):
        super().change()
        angle = self.line.line().angle()
        if self.triangleItem:
            self.triangleItem.setPos(self.line_end)
            self.triangleItem.setRotation(-angle + 90)


class ArrowLineWithWeight(ArrowLine, LineWithWeight):
    CLASS_NAME = "ArrowLineWithWeight"

    def __init__(self, start_item, end_item, parent=None):
        super().__init__(start_item, end_item, parent)


class LineEnum(enum.Enum):
    LINE = "Line"
    LINE_WITH_WEIGHT = "LineWithWeight"
    ARROW_LINE = "ArrowLine"
    ARROW_LINE_WITH_WEIGHT = "ArrowLineWithWeight"


class GraphicsLineItem:
    """工厂类"""
    line = {LineEnum.LINE: Line, LineEnum.LINE_WITH_WEIGHT: LineWithWeight,
            LineEnum.ARROW_LINE: ArrowLine, LineEnum.ARROW_LINE_WITH_WEIGHT: ArrowLineWithWeight}
    string_to_enum = {"Line": LineEnum.LINE, "LineWithWeight": LineEnum.LINE_WITH_WEIGHT,
                      "ArrowLine": LineEnum.ARROW_LINE, "ArrowLineWithWeight": LineEnum.ARROW_LINE_WITH_WEIGHT}

    @classmethod
    def new_line(cls, start_item: QGraphicsItem, end_item: QGraphicsItem, line_type: Union[LineEnum, str]):
        if isinstance(line_type, str):
            line_type = cls.string_to_enum[line_type]
        print(f"new line type is {line_type.value}")
        return cls.line[line_type](start_item, end_item)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QGraphicsEllipseItem
    from src.widgets.graphics_view import MyGraphicsView

    app = QApplication()
    view = MyGraphicsView()
    node1 = QGraphicsEllipseItem(0, 0, 30, 30)
    node2 = QGraphicsEllipseItem(0, 0, 30, 30)
    node1.setBrush(Qt.red)
    node2.setBrush(Qt.red)
    node1.setPos(10, 10)
    node2.setPos(300, 300)
    view.scene.addItem(node1)
    view.scene.addItem(node2)
    view.show()

    line_ = GraphicsLineItem.new_line(node1, node2, LineEnum.ARROW_LINE)
    view.scene.addItem(line_)
    # line_.set_weight("250")

    app.exec()
