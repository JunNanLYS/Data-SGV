import PySide6
from typing import Optional, Union

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QPen, QFont, QColor
from src.widgets.node_item import TextNodeItem
from src import tool


class GraphNode(TextNodeItem):
    def __init__(self, name: str, rect: Optional[QRect] = QRect(0, 0, 40, 40)):
        super(GraphNode, self).__init__(name, rect.x(), rect.y(), rect.width(), rect.height())
        self.edges = list()  # edge
        self._name = name  # 节点名称
        self.setZValue(1)

        self.node.setPen(Qt.NoPen)

    def add_edge(self, edge):
        """
        edge: Line, LineWithWeight, ArrowLine, ArrowLineWithWeight
        """
        self.edges.append(edge)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name
        self.text.setText(new_name)
        r = self.r
        w = self.text.boundingRect().center().x()
        h = self.text.boundingRect().center().y()
        self.text.setPos(r - w, r - h)

    def setPos(self, pos: Union[PySide6.QtCore.QPointF, PySide6.QtCore.QPoint]) -> None:
        super().setPos(pos)
        for line in self.edges:
            line.change()

    def __str__(self):
        return f"<GraphNode, id={id(self)}, name={self.name}>"

    def __repr__(self):
        return self.__str__()
