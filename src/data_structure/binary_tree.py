from typing import Optional, Any, Union

import PySide6
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsItemGroup, QGraphicsSimpleTextItem, \
    QGraphicsItemAnimation
from PySide6.QtCore import QRect, QPointF, QTimeLine
from PySide6.QtGui import QColor, QBrush
from src.widgets.line_item import Line
from src.tool import stop_time, JsonSettingTool
from src.widgets.node_item import TextNodeItem


class TreeNode(TextNodeItem):

    def __init__(self, val: str, rect: Optional[QRect] = QRect(0, 0, 30, 30)):
        super().__init__(val, rect.x(), rect.y(), rect.width(), rect.height())
        self.left: Optional[TreeNode] = None  # 左节点
        self.right: Optional[TreeNode] = None  # 右节点
        self.parent: Optional[TreeNode] = None  # 父节点
        self.l_line: Optional[Line] = None  # 连接左节点的线条
        self.r_line: Optional[Line] = None  # 连接右节点的线条
        self.p_line: Optional[Line] = None  # 连接父节点的线条

        self.val = val  # 节点值

    def cur_depth(self, root) -> int:
        """查找当前节点在树的第几层"""
        if root is None:
            return 0
        return 1 + self.cur_depth(root.parent)

    def itemChange(self, change: PySide6.QtWidgets.QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change is self.GraphicsItemChange.ItemVisibleHasChanged:
            if self.l_line:
                self.l_line.change()
            if self.r_line:
                self.r_line.change()
            if self.p_line:
                self.p_line.change()
        return super().itemChange(change, value)

    def max_depth(self, root) -> int:
        """最大深度"""
        if root is None:
            return 0
        return max(self.max_depth(root.left), self.max_depth(root.right)) + 1

    def move_animation(self, time: int, position: QPointF):
        """
        time is millisecond
        """
        animation = QGraphicsItemAnimation()
        timeLine = QTimeLine(time)  # 动画总时长
        animation.setItem(self)
        animation.setTimeLine(timeLine)
        animation.setPosAt(0, self.pos())
        animation.setPosAt(1, position)
        animation.timeLine().start()
        stop_time(1)

    def set_color(self, color: Union[QColor, str] = None) -> None:
        """修改节点颜色"""
        self.set_node_brush(color)

    def __str__(self):
        return f"val = {self.val}, l = {self.left}, r = {self.right}, binary_tree.TreeNode(id={id(self)}, pos={self.pos()})"
