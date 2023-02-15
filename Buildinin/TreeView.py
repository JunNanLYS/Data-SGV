import gc
import time

import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QCursor, QBrush, QColor, QPen
from PySide6.QtCore import Qt, QPointF, QTimeLine, QTime, QCoreApplication, QEventLoop, QPoint, Property, \
    QPropertyAnimation
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItemAnimation

from DataStructView.Buildinin.TreeItem import TreeNode, TreeLine


def stopTime(second: int):
    endTime = QTime.currentTime().addSecs(second)
    while QTime.currentTime() < endTime:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)


class TreeView(QGraphicsView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)

        # 初始化
        self.mouse = Qt.MouseButton.NoButton  # 记录鼠标事件
        self._enlarge = 0  # 放大的次数
        self._shrink = 0  # 缩小的次数
        self.last_pos = QtCore.QPointF()  # 作用 -> 记录鼠标位置，移动view
        self.select_node = None  # 选中的节点
        self.lock_node = None  # 锁定的节点
        self.interactive = True  # 场景交互

        # 设置Setting
        self.setScene(QGraphicsScene(self.x(), self.y(), self.width(), self.height(), self))  # 内置一个场景
        self.viewport().setProperty("cursor", QCursor(Qt.CrossCursor))  # 设置光标为十字型  ( + )

        self.default_node = TreeNode()
        self.scene().addItem(self.default_node)
        self.default_node.setPos(0, -300)
        self.default_node.curScene = self.scene()

        self.y_spacing = self.default_node.boundingRect().center().y() + 50  # y间距
        self.x_spacing = self.default_node.boundingRect().center().x()  # x间距
        self.ratio = 2  # 间距比例(数值越大)

    # 鼠标点击事件
    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        """
        左键：
            1. 第一次点击该节点
            2. 第二次点击该节点
        中键：
            1. 保存点击的位置用于移动视图
        右键：
            1. 右键被选中的节点 -> 删除
        详细内容：
        在用户左键点击一个节点时则选中该节点，若他再次点击该节点或者点击空白位置则取消选择
        用户选中一个节点后对该节点右键则会删除该节点，然后该节点下的所有节点都将被删除
        用户中键将记录点击的位置，长按可以移动视图
        """
        self.mouse = event.button()
        item = self.itemAt(event.pos())

        if self.interactive and item is None:
            if self.select_node: self.select_node.set_color('unselect')
            self.select_node = None
            self.lock_node = None

        if event.button() == Qt.MiddleButton:
            self.last_pos = self.mapToScene(event.pos())
            return
        # 可交互 & 鼠标左键
        elif self.interactive and event.button() == Qt.MouseButton.LeftButton:
            # 第一次点击该节点
            if type(item) == TreeNode and item != self.select_node:
                if self.select_node: self.select_node.set_color('unselect')
                self.select_node = item
                self.select_node.set_color('select')
            # 点击被选中的节点
            elif type(item) == TreeNode and item == self.select_node:
                # 点击的节点为被锁定的节点
                if item == self.lock_node:
                    if self.lock_node: self.lock_node.set_color('unselect')
                    self.lock_node = None
                    self.select_node = None
                    return
                # 未被锁定的节点
                self.lock_node = item
                if self.select_node: self.select_node.set_color('lock')
        # 可交互 & 鼠标右键
        elif self.interactive and event.button() == Qt.MouseButton.RightButton:
            if type(item) == TreeNode and item == self.lock_node:
                parent = item.parent
                # 将父节点的对应指针指向None
                if parent.left == item:
                    parent.left = None
                elif parent.right == item:
                    parent.right = None
                self.delete_node(item)

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if not self.interactive: return
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
            dp = self.mapToScene(event.pos()) - self.last_pos
            sRect = self.sceneRect()
            self.setSceneRect(sRect.x() - dp.x(), sRect.y() - dp.y(), sRect.width(), sRect.height())
            self.last_pos = self.mapToScene(event.pos())
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
        if directions != 'l' and directions != 'r':
            print("TreeView: createNode的directions传进了一个非'l'和'r'的directions")
            return
        new_node = self.get_newNode(node, directions)  # 新节点
        self.scene().addItem(new_node)
        new_node.setPos(self.calculated_pos(new_node, directions))
        # 线连接
        line = TreeLine(node, new_node)
        self.scene().addItem(line)
        line.curScene = self.scene()
        if directions == 'l':
            node.l_line = line
        else:
            node.r_line = line
        new_node.p_line = line
        # 当前节点为最后一层，要重新绘制所有节点的位置
        self.redraw()

    def redraw(self):
        """
        这个方法主要时防止二叉树节点的增多带来的交叉，只有在最后一层节点增加时才调用该方法
        """
        root = self.default_node
        q = []
        tree_max_layer = root.maxDepth()
        if root.left: q.append((root.left, 'l'))
        if root.right: q.append((root.right, 'r'))

        while q:
            temp = []
            for node, directions in q:
                node.max_layer = tree_max_layer
                node.setPos(self.calculated_pos(node, directions))
                self.change_node_line(node)
                if node.left:
                    temp.append((node.left, 'l'))
                if node.right:
                    temp.append((node.right, 'r'))
            q = temp

    # 创建一个新的节点并将数据处理好
    def get_newNode(self, node: TreeNode, directions: str) -> TreeNode:
        new_node = TreeNode()
        self.scene().addItem(new_node)
        new_node.parent = node
        new_node.curScene = self.scene()
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
        space_between = pow(self.ratio, node.max_layer - (node.cur_layer - 1)) - 2
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

    # 改变节点线条
    def change_node_line(self, node: TreeNode):
        if node.parent:
            node.p_line.change()
        if node.left:
            node.l_line.change()
        if node.right:
            node.r_line.change()

    def button_to_preorder(self):
        # 动画开始
        self.interactive = False
        self.traversal_color('start')

        self.preorder_traversal(self.select_node)  # 启动前序遍历

        # 动画结束
        self.traversal_color('end')
        self.interactive = True

    def button_to_inorder(self):
        # 动画开始
        self.interactive = False
        self.traversal_color('start')

        self.inorder_traversal(self.select_node)  # 启动中序遍历

        # 动画结束
        self.traversal_color('end')
        self.interactive = True

    def button_to_postorder(self):
        # 动画开始
        self.interactive = False
        self.traversal_color('start')

        self.postorder_traversal(self.select_node)  # 启动后序遍历

        # 动画结束
        self.traversal_color('end')
        self.interactive = True

    # 前序遍历
    def preorder_traversal(self, node: TreeNode) -> None:
        if node is None: return
        if node.p_line:
            node.p_line.traversal()
        node.traversal_animation()
        self.preorder_traversal(node.left)
        self.preorder_traversal(node.right)

    # 中序遍历
    def inorder_traversal(self, node: TreeNode):
        if node.left:
            self.inorder_traversal(node.left)
            node.l_line.traversal()
        node.traversal_animation()
        if node.right:
            self.inorder_traversal(node.right)
            node.r_line.traversal()

    # 后序遍历
    def postorder_traversal(self, node: TreeNode):
        if node.left:
            self.postorder_traversal(node.left)
            node.l_line.traversal()
        if node.right:
            self.postorder_traversal(node.right)
            node.r_line.traversal()
        node.traversal_animation()

    # 遍历前初始化
    def traversal_color(self, color_set: str):
        """
        color_set: 可以输入 'start' 和 'end' 两种参数

        start: 将节点及边颜色改为绿色以达到效果
        end: 将节点及边颜色还原
        """
        if color_set != 'start' and color_set != 'end':
            print("Error: color_set参数传入错误，请在 'start' 和 'end' 中选一个")
        root = self.default_node
        node_color = QBrush(QColor(0, 255, 0)) if color_set == 'start' else QBrush(QColor(58, 143, 192))
        line_color = QPen(QColor(0, 255, 0)) if color_set == 'start' else QPen(Qt.black, 3, Qt.SolidLine, Qt.RoundCap,
                                                                               Qt.RoundJoin)
        root.setBrush(node_color)
        q = []
        if root.left: q.append((root.left, 'l'))
        if root.right: q.append((root.right, 'r'))
        while q:
            temp = []
            for node, direction in q:
                node.setBrush(node_color)
                node.p_line.setPen(line_color)
                if node.left:
                    temp.append((node.left, 'l'))
                    node.l_line.setPen(line_color)
                if node.right:
                    temp.append((node.right, 'r'))
                    node.r_line.setPen(line_color)
            q = temp

    # 删除节点
    def delete_node(self, node):
        """
        删除的节点不能是初始节点(创建场景时就有的)
        用户删除节点后要将该节点下所有的节点以及边删除
        """
        if node == self.default_node:
            print("不能删除初始节点")
            return
        item = []

        def dfs(node: TreeNode):
            if node is None: return
            item.append(node)
            dfs(node.left)
            dfs(node.right)

        dfs(node)
        for x in item:
            self.scene().removeItem(x.p_line)
            self.scene().removeItem(x)

