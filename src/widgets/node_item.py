from typing import Optional, Any

from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtCore import QRect
from PySide6.QtGui import QColor, QBrush
from src.tool import ColorTool, PathTool
import path
import json


class NodeItem(QGraphicsEllipseItem):
    default_color = QBrush(QColor(58, 143, 192))  # 默认颜色(蓝色)
    select_color = QBrush(QColor(255, 0, 0))  # 红色

    def __init__(self, rect: Optional[QRect] = QRect(0, 0, 30, 30)):
        super(NodeItem, self).__init__(rect)
        with open(PathTool.get_setting_json_path(), 'r') as f:
            setting_dict = json.load(f)
        color = setting_dict['global']['node_color']
        self.node_color = QBrush(ColorTool.string_to_QColor(color))
        self.setBrush(self.node_color)

    def set_color(self, *args) -> None:
        raise NotImplementedError
