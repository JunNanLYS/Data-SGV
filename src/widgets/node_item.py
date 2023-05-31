from enum import Enum
from typing import Union

import PySide6
from PySide6 import QtCore
from PySide6.QtGui import QColor, QBrush, QFont, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItemGroup, QGraphicsSimpleTextItem


class NodeItem(QGraphicsItemGroup):
    DEFAULT_COLOR = QBrush(QColor(58, 143, 192))  # 默认颜色(蓝色)
    SELECTED_COLOR = QBrush(QColor(255, 0, 0))  # 红色

    def __init__(self, x=0, y=0, w=30, h=30, parent=None):
        super().__init__(parent)
        self.node = QGraphicsEllipseItem(x, y, w, h, self)  # 创建圆形
        self.r = self.node.boundingRect().center().x()

        # init node
        self.set_node_brush(self.DEFAULT_COLOR)

        # add to group
        self.addToGroup(self.node)

    def boundingRect(self) -> PySide6.QtCore.QRectF:
        """return node rect"""
        return self.node.rect()

    def set_node_brush(self, color: Union[QColor, str]):
        """set node brush"""
        self.node.setBrush(QBrush(color))

    def set_node_pen(self, pen: Union[QPen, QColor]):
        """ste node pen"""
        self.node.setPen(pen)


class TextNodeItem(NodeItem):
    def __init__(self, text: str, x=0, y=0, w=30, h=30, parent=None):
        super().__init__(x, y, w, h, parent)
        self.text = QGraphicsSimpleTextItem(text, self)
        # init text
        font = QFont()
        font.setPointSize(8)  # 字大小
        font.setFamily("Segoe")  # 字体
        self.text.setFont(font)
        self.text.setBrush(QBrush("black"))  # 字体颜色

        # add to group
        self.addToGroup(self.text)

        # 文本放置在圆心
        r = self.r
        w = self.text.boundingRect().center().x()
        h = self.text.boundingRect().center().y()
        self.text.setPos(r - w, r - h)

    def set_text_font(self, font: QFont) -> None:
        self.text.setFont(font)

    def set_text_brush(self, color: Union[QColor, str]) -> None:
        self.text.setBrush(QBrush(color))


class NodeEnum(Enum):
    NODE_ITEM = "NodeItem"
    TEXT_NODE_ITEM = "TextNodeItem"


class GraphicsEllipseItem:
    node = {NodeEnum.NODE_ITEM: NodeItem, NodeEnum.TEXT_NODE_ITEM: TextNodeItem}

    @classmethod
    def new_node(cls, node_type: NodeEnum, **kwargs):
        print(f"new node type is {node_type.value}")
        return cls.node[node_type](**kwargs)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene

    app = QApplication()

    view = QGraphicsView()
    view.resize(500, 500)
    scene = QGraphicsScene()
    view.setScene(scene)
    node = GraphicsEllipseItem.new_node(NodeEnum.TEXT_NODE_ITEM, text="hello")
    view.scene().addItem(node)
    view.show()

    app.exec()
