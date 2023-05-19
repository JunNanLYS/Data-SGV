from typing import Optional, Any

import PySide6
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsItemGroup, QGraphicsSimpleTextItem, \
    QGraphicsItemAnimation
from PySide6.QtCore import QRect, QPointF, QTimeLine
from PySide6.QtGui import QColor, QBrush
from ..widgets import line_item
from src.tool import ColorTool, stop_time, JsonSettingTool
from ..widgets.node_item import NodeItem


class TreeNode(QGraphicsItemGroup, NodeItem):

    def __init__(self, val: str, rect: Optional[QRect] = QRect(0, 0, 30, 30)):
        super(TreeNode, self).__init__()
        self.left: Optional[TreeNode] = None  # 左节点
        self.right: Optional[TreeNode] = None  # 右节点
        self.parent: Optional[TreeNode] = None  # 父节点
        self.l_line: Optional[line_item.LineToEllipse] = None  # 连接左节点的线条
        self.r_line: Optional[line_item.LineToEllipse] = None  # 连接右节点的线条
        self.p_line: Optional[line_item.LineToEllipse] = None  # 连接父节点的线条

        self.node = NodeItem(rect)
        self.val: str = val  # 节点值
        self.text: Optional[QGraphicsSimpleTextItem] = QGraphicsSimpleTextItem(self.val)

        # 将圆形与文本组合
        self.addToGroup(self.node)
        self.addToGroup(self.text)

        # 文本放置在圆心
        r = self.node.boundingRect().center().x()
        w = self.text.boundingRect().center().x()
        h = self.text.boundingRect().center().y()
        self.text.setPos(r - w, r - h)

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

    def move_animation(self, target: QPointF):
        """
        接收一个参数 target
        实现节点从一个点移动到另一个点的动画
        """
        time = int(JsonSettingTool.animation_speed() * 1000)
        animation = QGraphicsItemAnimation()
        timeLine = QTimeLine(time)  # 动画总时长
        animation.setItem(self)
        animation.setTimeLine(timeLine)
        animation.setPosAt(0, self.pos())
        animation.setPosAt(1, target)
        animation.timeLine().start()
        stop_time(1)

    def set_color(self, name: Optional[str] = None, color: Optional[QColor] = None) -> None:
        """修改节点颜色"""
        if name:
            self.node.setBrush(QBrush(ColorTool.string_to_QColor(name)))
        elif color:
            self.node.setBrush(QBrush(color))
        return

    def __str__(self):
        return f"val = {self.val}, l = {self.left}, r = {self.right}, binary_tree.TreeNode(id={id(self)}, pos={self.pos()})"
