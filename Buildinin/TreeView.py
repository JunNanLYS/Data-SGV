import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QCursor, QBrush, QColor, QPen
from PySide6.QtCore import Qt, QPointF, QTimeLine, QTime, QCoreApplication, QEventLoop, QPoint, Property, \
    QPropertyAnimation
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItemAnimation

from DataStructView.Buildinin.TreeItem import TreeNode


class TreeView(QGraphicsView):
    mouse = Qt.MouseButton.NoButton  # 记录鼠标事件
    _enlarge = 0  # 放大的次数
    _shrink = 0  # 缩小的次数
    lastPos = QtCore.QPointF()  # 作用 -> 记录鼠标位置，移动view

    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)

        # 设置Setting
        if not self.isInteractive(): print("MyGraphicsView: 没有开启场景交互功能")  # 判断有没有进行场景交互
        self.setScene(QGraphicsScene(self.x(), self.y(), self.width(), self.height(), self))  # 内置一个场景
        self.viewport().setProperty("cursor", QCursor(Qt.CrossCursor))  # 设置光标为十字型  ( + )

        self.default_node = TreeNode()
        self.scene().addItem(self.default_node)
        self.default_node.setPos(0, -300)

        self.y_spacing = self.default_node.boundingRect().center().y() + 50  # y间距
        self.x_spacing = self.default_node.boundingRect().center().x() + 0  # x间距

    # 鼠标点击事件
    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = event.button()
        if event.button() == Qt.MiddleButton:
            self.lastPos = self.mapToScene(event.pos())
            return

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        item = self.itemAt(event.pos())
        # 点击节点
        if item and type(item) == TreeNode:
            # 创建左孩子
            if event.button() == Qt.MouseButton.LeftButton:
                if item.left is None:
                    self.createNode(item, 'l')
                # print("双击左键")
            # 创建右孩子
            elif event.button() == Qt.MouseButton.RightButton:
                if item.right is None:
                    self.createNode(item, 'r')
                # print("双击右键")

    # 鼠标点击后长按移动事件
    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if self.mouse == Qt.MiddleButton:
            dp = self.mapToScene(event.pos()) - self.lastPos
            sRect = self.sceneRect()
            self.setSceneRect(sRect.x() - dp.x(), sRect.y() - dp.y(), sRect.width(), sRect.height())
            self.lastPos = self.mapToScene(event.pos())
            return
        QGraphicsView.mouseMoveEvent(self, event)

    # 滚轮
    def wheelEvent(self, event) -> None:
        # 等比例缩放
        wheelValue = event.angleDelta().y()
        ratio = wheelValue / 1200 + 1  # ratio -> 1.1 or 0.9
        if ratio > 1:  # 放大次数6
            if self._enlarge < 6:
                self._enlarge += 1
                self._shrink -= 1
                self.scale(ratio, ratio)
        else:  # 缩小次数10
            if self._shrink < 10:
                self._shrink += 1
                self._enlarge -= 1
                self.scale(ratio, ratio)

    # 鼠标释放事件
    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = Qt.MouseButton.NoButton

    def createNode(self, node: TreeNode, directions: str):
        # 当前节点为最后一层，要重新绘制所有节点的位置
        if node.cur_layer == node.max_layer and node != self.default_node:
            self.redraw()
        if directions != 'l' and directions != 'r':
            print("TreeView: createNode的directions传进了一个非'l'和'r'的directions")
            return
        new_node = self.__newNode(node, directions)  # 新节点
        self.scene().addItem(new_node)
        new_node.setPos(self.calculated_pos(new_node, directions))

    def redraw(self):
        root = self.default_node
        q = []
        # if root.max_layer == 0 or root.max_layer == 1: return
        if root.left: q.append((root.left, 'l'))
        if root.right: q.append((root.right, 'r'))

        while q:
            temp = []
            for node, directions in q:
                node.max_layer += 1
                node.setPos(self.calculated_pos(node, directions))
                if node.left:
                    temp.append((node.left, 'l'))
                if node.right:
                    temp.append((node.right, 'r'))
            q = temp

    # 创建一个新的节点并将数据处理好
    def __newNode(self, node: TreeNode, directions: str) -> TreeNode:
        new_node = TreeNode()
        self.scene().addItem(new_node)
        new_node.parent = node
        if directions == 'l':
            node.left = new_node
        else:
            node.right = new_node

        new_node.cur_layer = node.cur_layer + 1
        new_node.max_layer = max(new_node.cur_layer, node.max_layer)  # 当前层数与父节点取最大
        return new_node

    # 计算节点的坐标
    def calculated_pos(self, node: TreeNode, directions: str) -> QPointF:
        # 计算间隔比例
        space_between = pow(2, node.max_layer - (node.cur_layer - 1)) - 2
        # x坐标 = 父节点x坐标 +/- (间距比例 * x间隔) +/- 节点的半径
        # y坐标 = 父节点的y坐标 +/- 固定的行距
        r = node.boundingRect().center().x()
        x_parent = node.parent.pos().x()
        y_parent = node.parent.pos().y()
        x = x_parent - (space_between * self.x_spacing) - r if directions == 'l' else x_parent + (
                    space_between * self.x_spacing) + r
        y = y_parent + self.y_spacing
        pos = QPointF(x, y)
        return pos
