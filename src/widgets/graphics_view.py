import sys
import PySide6

from typing import Tuple, Optional, Union
from collections import defaultdict, deque
from PySide6.QtCore import QPoint, Property, QLineF, QPropertyAnimation, Qt, QPointF
from PySide6.QtGui import QCursor, QPainter, QTransform, QColor
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsSimpleTextItem, QGraphicsItem

from src.widgets import line_item
from src.data_structure.binary_tree import TreeNode
from src.data_structure.graph import GraphNode
from src.tool import JsonSettingTool, stop_time
from src.widgets.node_item import NodeItem

LINE_ITEMS = {line_item.Line, line_item.LineToEllipse, line_item.ArrowLine,
              line_item.ArrowLineWithWeight, line_item.LineWithWeight}


class MyGraphicsView(QGraphicsView):

    def __init__(self, parent=None):
        super(MyGraphicsView, self).__init__(parent)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)  # 抗锯齿 | 平滑像素
        self.scene = QGraphicsScene(self.x(), self.y(), self.width(), self.height())  # 内置场景
        self.viewport().setProperty("cursor", QCursor(Qt.CrossCursor))  # 设置光标为十字型  ( + )
        self.setScene(self.scene)

        # 初始化
        self.mouse: Optional[Qt.MouseButton] = Qt.MouseButton.NoButton  # 记录鼠标事件
        self.last_pos: Optional[QPoint, QPointF] = None  # 作用 -> 记录鼠标位置，移动view

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = event.button()
        if event.button() == Qt.MiddleButton:
            self.last_pos = self.mapToScene(event.position().toPoint())
            return

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if self.mouse == Qt.MiddleButton:
            dp = self.mapToScene(event.position().toPoint()) - self.last_pos
            sRect = self.sceneRect()
            self.setSceneRect(sRect.x() - dp.x(), sRect.y() - dp.y(), sRect.width(), sRect.height())
            self.last_pos = self.mapToScene(event.position().toPoint())
            return

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = Qt.MouseButton.NoButton

    def wheelEvent(self, event) -> None:
        zoomInFactor = 1.25  # 放大因子
        zoomOutFactor = 1 / zoomInFactor  # 缩小因子

        # 滚轮向上
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)  # 缩放

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        """让场景随着视图大小的变化而变化"""
        super().resizeEvent(event)
        new_rect = self.rect()
        self.scene.setSceneRect(new_rect)
        return

    def set_color(self, name: str = None, color: QColor = None) -> None:
        pass

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)


# 二叉树
class BinaryTreeView(MyGraphicsView):
    root_y = 50
    animation_line: Optional[line_item.LineToEllipse] = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.nodes = set()  # 节点集合

        self.y_spacing = TreeNode("").boundingRect().center().y() + 50  # y间距
        self.x_spacing = TreeNode("").boundingRect().center().x()  # x间距

        self._root: Optional[TreeNode] = None

    def add_node(self, val: str) -> None:
        """添加新节点"""
        # 已经存在相同的值了，不允许存在相同的值
        if val in self.nodes:
            print(f"add_node: {val} in nodes")
            # 这里最好加一个弹窗,或者消息窗
            return
        # val不为数字
        if not val.isdigit():
            print(f"add_node: {val} is not digit")
            # 消息窗(待加入)
            return
        self.create_node(val)
        pass

    def animation_line_start(self, line: Optional[line_item.LineToEllipse]):
        self.animation_line = line

        animation_speed: float = JsonSettingTool.animation_speed()  # 动画速度
        ms = int(animation_speed * 1000)  # 转毫秒
        anim = QPropertyAnimation(self, b'connect_line')
        anim.setStartValue(self.animation_line.line_start)
        anim.setEndValue(self.animation_line.line_end)
        anim.setDuration(ms)
        anim.start()
        stop_time(millisecond=ms)

    @Property(QPointF)
    def connect_line(self):
        return self.animation_line.line_end

    @connect_line.setter
    def connect_line(self, p: QPointF):
        self.animation_line.line_end = p
        line = QLineF(self.animation_line.line_start, self.animation_line.line_end)
        self.animation_line.setLine(line)

    def create_node(self, val: str):
        """创建节点"""
        # 没有根节点，创建一个根节点
        if not self.nodes:
            node = TreeNode(val)
            node.setPos(QPointF(self.root_x, self.root_y))
            self.scene.addItem(node)
            self._root = node
        else:
            parent, direction = self.search_insert_node(val)
            new_node = TreeNode(val)  # 新节点

            if direction == 'l':
                parent.left = new_node
            else:
                parent.right = new_node
            new_node.parent = parent

            pos = self.calculated_pos(new_node, direction)  # 计算新节点放置的位置
            new_node.setPos(pos)  # 放置节点
            self.scene.addItem(new_node)
            self.redraw_tree()

            self.connect_node(parent, new_node, direction)
        self.nodes.add(val)

    def connect_node(self, parent: TreeNode, child: TreeNode, direction: str) -> None:
        """连接节点"""
        line = line_item.LineToEllipse(parent, child)
        self.scene.addItem(line)
        self.animation_line_start(line)  # 连接节点
        child.p_line = line
        if direction == 'l':
            parent.l_line = line
        else:
            parent.r_line = line

    def calculated_pos(self, node: TreeNode, directions: str) -> QPointF:
        """计算节点放置位置"""
        # 计算间隔比例
        space_between = pow(2, node.max_depth(self.root) - (node.cur_depth(node) - 1)) - 2
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

    def delete_node(self, val: str):
        """删除节点"""
        del_node = self.search_node(val)
        del_pos = del_node.pos()
        del_left = del_node.left
        del_right = del_node.right
        del_parent = del_node.parent
        direction = 'l' if del_parent.left is del_node else 'r'
        if del_node is self.root:
            if del_right:
                self._root = del_right
            elif del_left:
                self._root = del_left

        # 删除节点以及线条
        del_item = [del_node, del_node.l_line, del_node.r_line, del_node.p_line]
        for item in del_item:
            if item:
                self.scene.removeItem(item)

        if del_right:
            del_right.move_animation(del_pos)  # 右节点移动到删除节点的位置
            node = del_right
            if del_left:
                while node.left is not None:
                    node = node.left
                del_left.parent = node
                del_left.p_line.start_item = node
                node.left = del_left
                node.l_line = del_left.p_line
            if del_parent:
                del_right.parent = del_parent
                del_right.p_line.start_item = del_parent

        elif del_left:
            del_left.move_animation(del_pos)

    def recover(self):
        """二叉树还原至初始状态"""
        pass

    @property
    def root_x(self):
        return self.scene.width() / 2

    @property
    def root(self) -> Optional[TreeNode]:
        pos = QPointF(self.root_x, self.root_y)
        return self.scene.itemAt(pos, QTransform())

    def redraw_tree(self):
        """重绘二叉树"""
        root: Optional[TreeNode] = None

        if self._root in self.scene.items():
            root = self._root
        elif self.root:
            root = self.root

        if root is None:
            return
        print("redraw_tree: 重绘二叉树")
        root.setPos(self.root_x, self.root_y)
        root.itemChange(root.GraphicsItemChange.ItemVisibleHasChanged, True)
        q = []
        if root.left:
            q.append((root.left, 'l'))
        if root.right:
            q.append((root.right, 'r'))
        while q:
            temp = []
            for node, direction in q:
                pos = self.calculated_pos(node, direction)
                node.setPos(pos)
                node.itemChange(root.GraphicsItemChange.ItemVisibleHasChanged, True)
                if node.left:
                    temp.append((node.left, 'l'))
                if node.right:
                    temp.append((node.right, 'r'))
            q = temp

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        new_rect = self.rect()
        self.setSceneRect(new_rect)
        self.redraw_tree()

    def search_insert_node(self, val: str) -> Tuple[TreeNode, str]:
        """查找节点插入位置，返回父节点以及插入方向"""

        def dfs(node: TreeNode):
            if int(val) < int(node.val):
                if node.left is None:
                    return node, 'l'
                return dfs(node.left)
            elif int(val) > int(node.val):
                if node.right is None:
                    return node, 'r'
                return dfs(node.right)
            else:
                raise TypeError(f"search_insert_node: {val} in nodes")

        if self._root in self.scene.items():
            root = self._root
        elif self.root:
            root = self.root
        else:
            raise TypeError("root not in scene items and self.root is None")
        return dfs(root)

    def search_node(self, target: str) -> TreeNode:
        """
        搜索节点

        主要体现从二叉树根节点查找到节点的过程
        1. DFS
        2. 动画
        3. 颜色
        """

        def dfs(node: TreeNode) -> TreeNode:
            if int(node.val) == int(target):
                node.set_color('red')
                return node
            elif int(node.val) < int(target):
                node.set_color('green')
                self.animation_line_start(node.r_line)
                return dfs(node.right)
            else:
                node.set_color('green')
                self.animation_line_start(node.l_line)
                return dfs(node.left)

        if self._root in self.scene.items():
            root = self._root
            return dfs(root)
        elif self.root:
            root = self.root
            return dfs(root)
        else:
            print("没有找到根节点")
            raise AttributeError("The root node was not found")


# 堆
class HeapView(MyGraphicsView):
    pass


# 图
class GraphView(MyGraphicsView):
    def __init__(self):
        super(GraphView, self).__init__()

        self.item_group = ItemGroup()
        self.nodes = defaultdict(GraphNode)  # name: GraphNode object
        names = [x for x in range(1, 1001)]
        self.node_default_names = deque(map(str, names))
        self.pre_item: Optional[GraphView, line_item.LineWithWeight] = None  # 存储地址
        self.cnt = 0

    def add_node(self, position: QPoint) -> GraphNode:
        """添加新节点"""
        new_node = GraphNode(self.node_default_names.popleft())
        self.nodes[new_node.name] = new_node
        self.scene.addItem(new_node)
        position = self.mapToScene(position)
        new_node.setPos(position - QPointF(new_node.r, new_node.r))
        return new_node

    def delete_item(self, delete_item: Union[GraphNode, line_item.Line]) -> None:
        state = 0  # 表示状态 0执行删除边逻辑, 1执行删除节点逻辑
        if isinstance(delete_item, GraphNode):
            state = 1
        self.scene.removeItem(delete_item)  # 将其从场景中删除

        # 遍历所有与要被删除节点有关的item
        for item in self.item_group.find(delete_item):
            if isinstance(item, GraphNode):
                self.item_group.pop_item(item, delete_item)
                # delete_node is GraphNode
                if state:
                    item.pop_node(delete_item)
                # delete_node is Line
                else:
                    item.pop_line(delete_item)
            elif isinstance(item, line_item.Line):
                self.item_group.pop_item(item, delete_item)
                if state:
                    # 所有与delete_item有关的line都要从scene中删除
                    self.scene.removeItem(item)
                    if self.item_group.key_in_group(item):
                        for disconnect_item in self.item_group.find(item):
                            self.item_group.pop_item(disconnect_item, item)
                    self.item_group.pop(item)
                else:
                    print(f"在delete_item为line的情况下不应该出现连接同为line的item，检查item_group")
            else:
                TypeError(f"delete_item: item is {item}")

        self.item_group.pop(delete_item)

    def connect_node(self, name1: str, name2: str, state=line_item.LineEnum.LineWithWeight) -> None:
        node1, node2 = self.nodes[name1], self.nodes[name2]
        if self.item_group.in_group(node1, node2):
            return
        new_line = self.create_line(node1, node2, state)
        self.scene.addItem(new_line)
        node2.connect(node1, new_line)
        node1.connect(node2, new_line)
        self.item_group.add_items(node1, node2, new_line)

    def create_line(self, node1, node2, state: line_item.LineEnum = line_item.LineEnum.ArrowLineWithWeight):
        """
        return Optional[LineToEllipse, LineWithWeight, ArrowLine, ArrowLineWithWeight]
        """
        if state == line_item.LineEnum.LineToEllipse:
            new_line = line_item.LineToEllipse(node1, node2)
        elif state == line_item.LineEnum.ArrowLine:
            new_line = line_item.ArrowLine(node1, node2)
        elif state == line_item.LineEnum.ArrowLineWithWeight:
            new_line = line_item.ArrowLineWithWeight(node1, node2)
        elif state == line_item.LineEnum.LineWithWeight:
            new_line = line_item.LineWithWeight(node1, node2)
        else:
            raise TypeError(f"create_line: state is {state}")
        return new_line

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        event_pos = event.position().toPoint()
        event_item: Optional[NodeItem, QGraphicsSimpleTextItem] = self.itemAt(event_pos)
        if event_item:
            event_item = event_item.group()

        if self.mouse is Qt.MouseButton.LeftButton:
            # 点击节点
            if isinstance(event_item, GraphNode):
                if event_item is self.pre_item:
                    self.pre_item.switch_mode("creator")
                    return
                # 第一次点击该节点
                else:
                    # 有节点处于creator模式且点击另外一个节点
                    if self.pre_item and self.pre_item.mode == "creator":
                        self.pre_item.switch_mode("default")
                        self.connect_node(self.pre_item.name, event_item.name)
                    elif self.pre_item:
                        self.pre_item.switch_mode("default")
                    self.pre_item = event_item
                    self.pre_item.switch_mode("selected")
                    return
            # 点击边
            elif isinstance(event_item, line_item.Line):
                pass
            elif event_item is None:
                # 创建新节点
                if self.pre_item and type(self.pre_item) is GraphNode and self.pre_item.mode == "creator":
                    self.pre_item.switch_mode("default")
                    new_node = self.add_node(event_pos)
                    self.connect_node(self.pre_item.name, new_node.name)
                    self.pre_item = None
                else:
                    if self.pre_item and type(self.pre_item) is GraphNode:
                        self.pre_item.switch_mode("default")
                    self.pre_item = None
                    self.add_node(event_pos)
                return
        elif self.mouse is Qt.MouseButton.RightButton:
            if self.pre_item and type(self.pre_item) is GraphNode:
                self.pre_item.switch_mode("default")
                self.pre_item = None

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        event_pos = event.position().toPoint()
        event_pos_scene = self.mapToScene(event_pos)
        if self.mouse is Qt.MouseButton.LeftButton and self.pre_item:
            self.pre_item.setPos(event_pos_scene - QPointF(self.pre_item.r, self.pre_item.r))

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(event)


class ItemGroup:
    def __init__(self):
        self.__items = defaultdict(list)

    def add_item(self, key, value) -> None:
        self.__items[key].append(value)
        self.__items[value].append(key)
        return

    def add_items(self, key, value, *args) -> None:
        self.add_item(key, value)
        for value in args:
            self.add_item(key, value)
        return

    def key_in_group(self, key) -> bool:
        """若key在group中返回True,反之返回False"""
        return key in self.__items

    def find(self, key) -> list:
        return self.__items[key]

    def pop(self, key) -> None:
        """删除单个key"""
        self.__items.pop(key)
        return

    def pops(self, *args) -> None:
        """删除多个key"""
        for key in args:
            self.__items.pop(key)
        return

    def pop_item(self, key, items: Union[list, tuple, QGraphicsItem]) -> None:
        """删除key中的item"""
        if isinstance(items, (list, tuple)):
            for i, item in enumerate(items):
                self.__items[key].pop(i)
        elif isinstance(items, QGraphicsItem):
            for i, item in enumerate(self.__items[key]):
                if item is items:
                    self.__items[key].pop(i)
                    break
        else:
            raise TypeError(f"pop_item: items is {items}, type is {type(items)}")
        return

    def in_group(self, key, item) -> bool:
        """判断某个item是否在key组别中"""
        return item in self.__items[key]

    @property
    def grop(self) -> defaultdict:
        return self.__items


if __name__ == '__main__':
    # -----------二叉树----------
    # app = QApplication(sys.argv)
    # view = BinaryTreeView()
    # view.show()
    # view.resize(500, 500)
    # view.add_node('10')
    # view.add_node('20')
    # view.add_node('5')
    # view.add_node("15")
    # view.add_node("25")
    # view.add_node("7")
    # view.search_node('15')
    # sys.exit(app.exec())

    # ------------图-------------
    app = QApplication(sys.argv)
    view = GraphView()
    ZheJiang = GraphNode('Name1')
    ShangHai = GraphNode('Name2')
    view.scene.addItem(ZheJiang)
    view.scene.addItem(ShangHai)
    view.nodes['Name1'] = ZheJiang
    view.nodes['Name2'] = ShangHai
    ZheJiang.setPos(QPointF(300, 100))
    ShangHai.setPos(QPointF(400, 100))
    view.connect_node("Name1", "Name2")
    # line = line_item.ArrowLineWithWeight(ZheJiang, ShangHai)
    # view.scene.addItem(line)

    view.show()
    sys.exit(app.exec())
