# relative
import json

import PySide6
from typing import Optional, Union

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QPen, QFont, QColor
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsSimpleTextItem
from collections import defaultdict
from ..widgets.node_item import NodeItem
from src import tool


class GraphNode(QGraphicsItemGroup, NodeItem):
    def __init__(self, name: str, rect: Optional[QRect] = QRect(0, 0, 40, 40)):
        super(GraphNode, self).__init__()
        self.__connected_nodes = defaultdict(GraphNode)  # 存储连接的节点  name: node
        self.__connected_lines = list()  # 存储与该节点连接的线
        self.mode = "default"

        self.node = NodeItem(rect)  # 节点
        self.node.setPen(Qt.NoPen)
        self.name = name  # 节点名称
        self.text = QGraphicsSimpleTextItem(name)  # 文本
        self.update_node()  # 根据设置更新
        self.r = self.node.boundingRect().center().x()  # 半径

        # 将圆形与文本组合
        self.addToGroup(self.node)
        self.addToGroup(self.text)

        # 文本放置在圆心
        r = self.node.boundingRect().center().x()
        w = self.text.boundingRect().center().x()
        h = self.text.boundingRect().center().y()
        self.text.setPos(r - w, r - h)

    def boundingRect(self) -> PySide6.QtCore.QRectF:
        return self.node.boundingRect()

    def add_node(self, node: "GraphNode") -> None:
        """node: GraphNode"""
        self.connected_nodes[node.name] = node
        return

    def add_line(self, line) -> None:
        """line: Optional[LineToEllipse, ArrowLine, LineWithWeight, ArrowLineWithWeight]"""
        self.connected_lines.append(line)
        return

    def connect(self, node, line):
        self.add_node(node)
        self.add_line(line)

    @property
    def connected_nodes(self) -> defaultdict:
        return self.__connected_nodes

    @property
    def connected_lines(self) -> list:
        return self.__connected_lines

    def disconnect(self, node: "GraphNode", line) -> None:
        self.pop_node(node)
        self.pop_line(line)
        return

    def pop_node(self, node: Union[str, "GraphNode"]) -> None:
        # 传入的是node名字
        if isinstance(node, str):
            self.connected_nodes.pop(node)
            return
        self.connected_nodes.pop(node.name)

    def pop_line(self, line) -> None:
        self.connected_lines.remove(line)
        return

    def update_node(self):
        """
        依据setting配置文件来更新节点
        """
        with open(tool.PathTool.get_setting_json_path(), 'r') as f:
            setting = json.load(f)
        font_color = setting["graph"]["font_color"]
        font_size = setting["graph"]["font_size"]
        font_family = setting["graph"]["font_family"]

        font = QFont()
        font.setPointSize(font_size)  # 字体大小
        font.setFamily(font_family)  # 字体类型,宋体,楷体等
        self.text.setFont(font)
        self.text.setBrush(tool.ColorTool.string_to_QColor(font_color))  # 设置字体颜色

    def switch_mode(self, mode: str):
        if mode == "default":
            self.node.setPen(Qt.NoPen)
            self.node.setBrush(self.node.node_color)
            self.mode = "default"
        elif mode == "selected":
            self.node.setPen(QPen(tool.ColorTool.string_to_QColor("gray"), 3.5))
            self.mode = "selected"
        # creator
        else:
            self.node.setBrush(tool.ColorTool.string_to_QColor('red'))
            self.node.setPen(tool.ColorTool.string_to_QColor("green"))
            self.mode = "creator"

    def set_color(self, name: str = None, color: Optional[QColor] = None) -> None:
        if name:
            self.node.setBrush(tool.ColorTool.string_to_QColor(name))
        elif color:
            self.node.setBrush(color)
        return

    def setPos(self,
               pos: Union[PySide6.QtCore.QPointF, PySide6.QtCore.QPoint, PySide6.QtGui.QPainterPath.Element]) -> None:
        super().setPos(pos)
        for line in self.connected_lines:
            line.change()
