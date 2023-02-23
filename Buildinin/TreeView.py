import gc
import time

import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QCursor, QBrush, QColor, QPen
from PySide6.QtCore import Qt, QPointF, QTimeLine, QTime, QCoreApplication, QEventLoop, QPoint, Property, \
    QPropertyAnimation, QLineF
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItemAnimation, QGraphicsTextItem

from DataStructView.Buildinin.TreeItem import TreeNode, TreeLine, SearchTreeNode
from DataStructView.Class.MyGraphicsView import MyTreeView


def stopTime(second: int):
    endTime = QTime.currentTime().addSecs(second)
    while QTime.currentTime() < endTime:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)


class TreeView(MyTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)

        # 初始化
        self.mouse = Qt.MouseButton.NoButton  # 记录鼠标事件
        self._enlarge = 0  # 放大的次数
        self._shrink = 0  # 缩小的次数
        self.last_pos = QtCore.QPointF()  # 作用 -> 记录鼠标位置，移动view
        self.select_node = None  # 选中的节点
        self.lock_node = None  # 锁定的节点
        self.cur_line = None  # 用于线条连接

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

        self.interactive = True  # 场景交互

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
        self.mouse = event.button()  # 鼠标按键
        item = self.itemAt(event.pos())  # 项

        if self.interactive and item is None:
            self.unselect_node()

        if event.button() == Qt.MiddleButton:
            self.last_pos = self.mapToScene(event.pos())
            return
        # 可交互 & 鼠标左键
        elif self.interactive and event.button() == Qt.MouseButton.LeftButton:
            # 第一次点击该节点
            if type(item) == TreeNode and item != self.select_node:
                self.unselect_node()
                self.select_node = item
                self.select_node.set_color('select')
            # 点击被选中的节点
            elif type(item) == TreeNode and item == self.select_node:
                # 点击的节点为被锁定的节点
                if item == self.lock_node:
                    self.unselect_node()
                    return
                # 未被锁定的节点
                self.lock_node = item
                if self.select_node: self.select_node.set_color('lock')
                self.lock_node.lock_animation()
        # 可交互 & 鼠标右键
        elif self.interactive and event.button() == Qt.MouseButton.RightButton:
            if type(item) == TreeNode and item == self.lock_node:
                if item == self.default_node: return
                parent = item.parent
                # 将父节点的对应指针指向None
                if parent.left == item:
                    parent.left = None
                elif parent.right == item:
                    parent.right = None
                self.delete_node(item)
                self.unselect_node()
                return

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
                    self.unselect_node()
                # print("双击左键")
            # 创建右孩子
            elif event.button() == Qt.MouseButton.RightButton:
                if item.right is None:
                    self.createNode(item, 'r')
                    self.unselect_node()
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
        new_node.max_layer = new_node.maxDepth()  # 当前层数与父节点取最大
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
        self.unselect_node()

    def button_to_inorder(self):
        # 动画开始
        self.interactive = False
        self.traversal_color('start')

        self.inorder_traversal(self.select_node)  # 启动中序遍历

        # 动画结束
        self.traversal_color('end')
        self.interactive = True
        self.unselect_node()

    def button_to_postorder(self):
        # 动画开始
        self.interactive = False
        self.traversal_color('start')

        self.postorder_traversal(self.select_node)  # 启动后序遍历

        # 动画结束
        self.traversal_color('end')
        self.interactive = True
        self.unselect_node()

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

    # 将节点从选中状态和锁定状态切换至无状态
    def unselect_node(self):
        if self.select_node:
            self.select_node.set_color('unselect')
            self.select_node = None

        if self.lock_node:
            self.lock_node.set_color('unselect')
            self.lock_node = None


# 二叉搜索树View
class BinarySearchTreeView(MyTreeView):
    """
    只要实现添加、删除、搜索就行，遍历已经被TreeView实现了。
    """

    def __init__(self, parent=None):
        super(BinarySearchTreeView, self).__init__(parent)

        # 初始化
        self.node_vals = set()
        self.first_node = None
        self.default_node = SearchTreeNode("")  # 用于计算半径
        self.y_spacing = self.default_node.boundingRect().center().y() + 50  # y间距
        self.x_spacing = self.default_node.boundingRect().center().x()  # x间距
        self.ratio = 2  # 间距比例(数值越大)

    def add(self, s: str) -> None:
        """
        从lineEdit中获取要添加的节点的值
        若s中有多个值，则一个一个慢慢添加
        使用SearchTreeNode 将值以及要添加的位置传递给它
        """
        if not s: return
        val = self.split(s)
        for v in val:
            self.create_node(v)

    # 重绘
    def redraw(self):
        """
        这个方法主要时防止二叉树节点的增多带来的交叉，只有在最后一层节点增加时才调用该方法
        """
        root = self.first_node
        q = []
        tree_max_layer = root.maxDepth()
        if root.left: q.append((root.left, 'l'))
        if root.right: q.append((root.right, 'r'))

        while q:
            temp = []
            for node, directions in q:
                node.max_layer = tree_max_layer
                node.setPos(self.calculated_pos(node, directions))
                if node.left:
                    temp.append((node.left, 'l'))
                if node.right:
                    temp.append((node.right, 'r'))
            q = temp

    def get_node(self, parent_node: SearchTreeNode, directions: str, val: str) -> SearchTreeNode:
        """
        1. 返回新的树节点
        2. 将父节点与新节点连接
        3. 将节点连接
        """
        if directions != "l" and directions != "r":
            raise TypeError("direction can only 'l' or 'r'")
        new_node = SearchTreeNode(val)
        new_node.parent = parent_node
        new_line = TreeLine(parent_node, new_node)
        new_node.p_line = new_line
        if directions == "l":
            parent_node.left = new_node
            parent_node.l_line = new_line
        else:
            parent_node.right = new_node
            parent_node.r_line = new_line

        new_node.cur_layer = parent_node.cur_layer + 1
        new_node.max_layer = self.first_node.maxDepth()
        return new_node

    # 创建节点
    def create_node(self, val: str) -> None:
        if val in self.node_vals: return
        self.node_vals.add(val)
        parent_node, directions = self.insert_node(val)
        # 二叉搜索树的第一个节点，固定在某一个位置上
        if (not parent_node) and (not directions):
            pos = QPointF(0, -300)
            new_node = SearchTreeNode(val)
            new_node.setPos(pos)
            self.scene().addItem(new_node)
            self.scene().addItem(new_node.val)
            self.node_vals.add(val)
            self.first_node = new_node
            return
        new_node = self.get_node(parent_node, directions, val)
        pos = self.calculated_pos(new_node, directions)
        new_node.setPos(pos)

        # 将节点 & 值 & 线条 添加至场景
        self.scene().addItem(new_node)
        self.scene().addItem(new_node.val)
        self.scene().addItem(new_node.p_line)

        self.redraw()

    # 计算两个节点的极角坐标
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

    # 查找插入位置
    def insert_node(self, val: str):
        """
        插入方法
        查找节点插入的位置同时完成插入

        若该为第一个节点则在插入至默认位置
        """

        # 查找插入位置
        def insert_position(node: SearchTreeNode, cur_val: str):
            if int(cur_val) < int(node.val.text()):
                if node.left is None: return node, "l"
                return insert_position(node.left, cur_val)
            elif int(cur_val) > int(node.val.text()):
                if node.right is None: return node, "r"
                return insert_position(node.right, cur_val)
            else:
                raise TypeError("insert_position: 不应该传入相同的值")

        # 第一个节点
        if not self.first_node:
            return "", ""
        else:
            return insert_position(self.first_node, val)

    def delete(self, val: str) -> None:
        """
        该方法不返回任何值

        1. 找到要delete的node
        2. node与父节点断开连接
        3. 删除node
        4. 处理node的子树
            1. 若node左右非空 -> 右子树替代原node位置，不断找右子树的最左节点，将原node的左子树连接
            2. 若node左空 -> 连接右子树
            3. 若node右空 -> 连接左子树
        5. node下的所有节点的 cur_layer 要-1
        6. 二叉搜索树所有节点的 max_layer 要重新赋值

        在删除节点的过程中要进行动画以达到效果
        1. 原node被删除
        2. 将要连接的子树移动到原node的位置
        3. 连接子树

        在该方法运行结束时要记得重绘二叉搜索树，因为二叉搜索树可能会因为delete，其最大深度可能会变大
        """

        # 辅助函数，用于搜索要被删除的节点
        def dfs(node: SearchTreeNode) -> SearchTreeNode:
            cur_val = node.val.text()
            if cur_val == val:
                return node
            elif cur_val < val:
                return dfs(node.right)
            else:
                return dfs(node.left)

        def delete_node_data(node: SearchTreeNode) -> str:
            """
            这是一个辅助函数，减少重复代码，将节点间的连接断开
            移除节点相关的item
            返回一个node在parent的哪个方向
            """
            parent = node.parent
            node.parent = None
            node.left = None
            node.right = None
            direction = ""

            # 与父节点断开
            if parent.left == node:
                parent.left = None
                parent.l_line = None
                direction = "l"
            elif parent.right == node:
                parent.right = None
                parent.r_line = None
                direction = "r"
            else:
                # 不应该出现这种情况
                # 父节点左或者右一定是要删除的node
                raise TypeError("The left and right nodes of the parent node are not the nodes to be deleted")

            # 删除节点相关
            if node.l_line:  # 左线
                self.scene().removeItem(node.l_line)
            if node.r_line:  # 右线
                self.scene().removeItem(node.r_line)
            if node.p_line:  # 父线
                self.scene().removeItem(node.p_line)
            self.scene().removeItem(node.val)  # 值
            self.scene().removeItem(node)  # 节点

            return direction

        node = dfs(self.first_node)  # 要删除的节点
        pos = node.pos()  # 节点位置

        # 将下面的节点接上
        if node.left and node.right:
            connect = node.right  # 替代原节点
            cur = node.right  # 右节点的最左端
            while cur.left:
                cur = cur.left
            node.delete_animation()  # 删除动画
            delete_node_data(node)  # 清除该节点相关的数据

        elif not node.left:
            ...
        elif not node.right:
            ...
        else:
            # 不应该出现这种情况
            # 以上已经枚举了所有情况了
            raise TypeError

    def search(self):
        ...

    def split(self, s: str) -> list[str]:
        i, n = 0, len(s)
        res = []
        while i < n:
            c = s[i]
            num = ""
            if c != ',' and c != '，' and (not c.isdigit()):
                print("错误字符")
                return []
                # raise TypeError("not digit and comma")
            while i < n and c.isdigit():
                c = s[i]
                num += c
                i += 1
            while i < n and c == ',' or c == '，':
                c = s[i]
                i += 1
            if num: res.append(num)
        return res
