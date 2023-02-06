import PySide6
from PySide6.QtCore import Qt,QPointF
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPathItem, QGraphicsItem


# 节点基类
class MyEllipseItem(QGraphicsEllipseItem):
    defaultBrush = QBrush(QColor(58, 143, 192))  # 默认颜色
    mouse = Qt.MouseButton.NoButton  # 记录鼠标事件

    def __init__(self, x=0, y=0, w=30, h=30, parent=None):
        super(MyEllipseItem, self).__init__(x, y, w, h, parent)

        # 设置Setting
        self.setAcceptDrops(True)
        self.setBrush(self.defaultBrush)  # 设置节点颜色
        self.setPen(Qt.NoPen)  # 关闭节点边缘线

    def mousePressEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.mouse = event.button()

    def mouseMoveEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        x, y = event.pos().x(), event.pos().y()
        if self.mouse == Qt.MouseButton.LeftButton:
            r = self.boundingRect().center().x()
            self.moveBy(x - r, y - r)  # 跟随鼠标移动位置
        self.setAcceptDrops(False)

    def mouseReleaseEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        self.mouse = Qt.MouseButton.NoButton
        self.setAcceptDrops(True)
        QGraphicsItem.mouseReleaseEvent(self, event)


# 直线基类
class MyLineItem(QGraphicsLineItem):
    mouse = Qt.MouseButton.NoButton

    def __init__(self, p1: QPointF, p2:QPointF, parent=None):
        super(MyLineItem, self).__init__(p1.x(), p1.y(), p2.x(), p2.y(), parent)



# 箭头直线基类
class MyArrowLine(QGraphicsPathItem):
    ...
