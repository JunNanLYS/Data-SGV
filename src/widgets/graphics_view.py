import sys
from collections import defaultdict, deque
from datetime import datetime
from typing import Tuple, Optional, Union

import PySide6
from PySide6.QtCore import QPoint, Property, QPropertyAnimation, Qt, QPointF, Signal
from PySide6.QtGui import QCursor, QPainter, QTransform, QColor, QFont
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QGraphicsItem

from src.data_structure.binary_tree import TreeNode
from src.data_structure.graph import GraphNode
from src.tool import stop_time
from src.widgets.line_item import GraphicsLineItem, Line, LineEnum, ArrowLine
from src.widgets.node_item import NodeModeEnum


class MyGraphicsView(QGraphicsView):
    log = Signal(str)
    diaLog = Signal(str, str)

    def __init__(self, parent=None):
        super(MyGraphicsView, self).__init__(parent)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)  # 抗锯齿 | 平滑像素
        self.scene = QGraphicsScene(self.x(), self.y(), self.width(), self.height())  # 内置场景
        self.viewport().setProperty("cursor", QCursor(Qt.CrossCursor))  # 设置光标为十字型  ( + )
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # init
        self.mouse: Optional[Qt.MouseButton] = Qt.MouseButton.NoButton  # 记录鼠标事件
        self.last_pos: Optional[QPoint, QPointF] = None  # 作用 -> 记录鼠标位置，移动view
        self.mouse_time = datetime.now()

        self.setStyleSheet(
            """
            border-radius: 10px;
            background-color: rgb(255, 255, 255);
            """
        )

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

    def mouseDoubleClickEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouseReleaseEvent(event)

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
    def __init__(self, parent=None):
        super().__init__(parent)
        # init config
        self.animation_time = 1000  # millisecond
        self.font_size = 8
        self.font_color = "black"

        # init
        self.nodes = set()  # 节点集

        self.root_y = 50
        self.y_spacing = TreeNode("").boundingRect().center().y() + 50  # y间距
        self.x_spacing = TreeNode("").boundingRect().center().x()  # x间距

        self._root: Optional[TreeNode] = None

        # animation
        self.animation_line: Optional[Line] = None

    def add_node(self, vals: Union[str, list]) -> None:
        """添加新节点"""

        def add(value):
            # 已经存在相同的值了，不允许存在相同的值
            value = value.replace(" ", "")  # 清除空格
            if value in self.nodes:
                print(f"add_node: {value} in nodes")
                self.diaLog.emit("Tip", "The same value exists")
                return
            # val不为数字
            if not value.isdigit():
                print(f"add_node: {value} is not digit")
                self.diaLog.emit("Error", f"{value} is not digit")
                return
            self.create_node(value)

        if isinstance(vals, list):
            for val in vals:
                add(val)
        else:
            add(vals)

    def animation_line_start(self, line: Optional[Line]):
        self.animation_line = line

        anim = QPropertyAnimation(self, b'connect_line')
        anim.setStartValue(self.animation_line.line_start)
        anim.setEndValue(self.animation_line.line_end)
        anim.setDuration(self.animation_time)
        anim.start()
        stop_time(millisecond=self.animation_time)

    def config(self, config_dict: dict) -> None:
        global_config = config_dict['global']
        local_config = config_dict['tree']
        animation_speed = global_config['animation_speed']
        font_size = local_config['font_size']
        font_color = local_config['font_color']

        self.animation_time = animation_speed * 1000
        self.font_size = font_size
        self.font_color = font_color

        self.redraw()


    @Property(QPointF)
    def connect_line(self):
        return self.animation_line.line_end

    @connect_line.setter
    def connect_line(self, p: QPointF):
        self.animation_line.line_end = p

    def create_node(self, val: str):
        """创建节点"""
        # 没有根节点，创建一个根节点
        self.log.emit(f"create new node {val}")
        if not self.nodes:
            node = self.new_node(val)
            node.setPos(QPointF(self.root_x, self.root_y))
            self.scene.addItem(node)
            self._root = node
        else:
            parent, direction = self.search_insert_node(val)
            new_node = self.new_node(val)  # 新节点

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

    def new_node(self, val: str) -> TreeNode:
        """
        set node
        return new node
        """
        res_node = TreeNode(val)
        font = QFont()
        font.setPointSize(self.font_size)
        res_node.set_text_font(font)
        res_node.set_text_brush(self.font_color)

        return res_node

    def connect_node(self, parent: TreeNode, child: TreeNode, direction: str) -> None:
        """连接节点"""

        line = GraphicsLineItem.new_line(parent, child, LineEnum.LINE)
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
        if del_parent and del_parent.left and del_parent.left is del_node:
            direction = 'l'
        elif del_parent and del_parent.right and del_parent.right is del_node:
            direction = 'r'

        if del_node is self.root:
            if del_right:
                self._root = del_right
            elif del_left:
                self._root = del_left

        # 删除节点以及线条
        del_item = [del_node, del_node.l_line, del_node.r_line, del_node.p_line]
        self.nodes.remove(val)
        for item in del_item:
            if item:
                self.scene.removeItem(item)
        del_node.delete_data()
        if del_parent:
            del_parent.disconnect(del_node)
        if del_left:
            del_left.disconnect(del_node)
        if del_right:
            del_right.disconnect(del_node)

        if del_right:
            del_right.move_animation(self.animation_time, del_pos)  # 右节点移动到删除节点的位置
            node = del_right
            if del_left:
                while node.left is not None:
                    node = node.left
                del_left.parent = node
                node.left = del_left
                self.connect_node(node, del_left, 'l')
            if del_parent:
                if direction == 'l':
                    del_parent.left = del_right
                else:
                    del_parent.right = del_right
                del_right.parent = del_parent
                self.connect_node(del_parent, del_right, direction)

        elif del_left:
            del_left.move_animation(self.animation_time, del_pos)
            if del_parent:
                if direction == 'l':
                    del_parent.left = del_left
                else:
                    del_parent.right = del_left
                del_left.parent = del_parent
                self.connect_node(del_parent, del_left, direction)
        self.redraw_tree()

    def redraw(self):
        root = self.root
        if root is None:
            return
        q = [root]
        font = QFont()
        font.setPointSize(self.font_size)

        while q:
            temp = []
            for node in q:
                node.switch_mode(NodeModeEnum.DEFAULT)
                node.set_text_brush(self.font_color)
                node.set_text_font(font)
                if node.left:
                    temp.append(node.left)
                if node.right:
                    temp.append(node.right)
            q = temp
        stop_time(millisecond=100)

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
        print(f"root: {root.cur_depth(root)}")
        print(f"_root: {self._root.cur_depth(self._root)}")
        root.setPos(QPointF(self.root_x, self.root_y))
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
            node.switch_mode(NodeModeEnum.PATH)
            if int(val) < int(node.val):
                if node.left is None:
                    self.log.emit("insert")
                    return node, 'l'
                self.log.emit("search left")
                return dfs(node.left)
            elif int(val) > int(node.val):
                if node.right is None:
                    self.log.emit("insert")
                    return node, 'r'
                self.log.emit("search right")
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
                node.switch_mode(NodeModeEnum.SELECTED)
                return node
            elif int(node.val) < int(target):
                node.switch_mode(NodeModeEnum.PATH)
                self.animation_line_start(node.r_line)
                return dfs(node.right)
            else:
                node.switch_mode(NodeModeEnum.PATH)
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

    @property
    def root_x(self):
        return self.scene.width() / 2

    @property
    def root(self) -> Optional[TreeNode]:
        pos = QPointF(self.root_x, self.root_y)
        return self.scene.itemAt(pos, QTransform())


# 堆
class HeapView(MyGraphicsView):
    pass


# 图
class GraphView(MyGraphicsView):
    clickedItem = Signal(int)  # 0 is line, 1 is node
    nodeInfo = Signal(int, str)
    edgeInfo = Signal(int, str, str, str, str)
    diaLog = Signal(str, str)

    def __init__(self):
        super(GraphView, self).__init__()
        # init config
        self.animation_time = 1000  # millisecond
        self.font_color = "black"  # font color
        self.font_size = 8  # font size
        self.font_family = "Segoe"  # font family
        self.node_color = GraphNode.DEFAULT_COLOR  # node color
        self.edge_type = "ArrowLineWithWeight"
        # -----------------------------------------------------

        self.item_group = ItemGroup()
        self.nodes = defaultdict(GraphNode)  # name: GraphNode object
        self.animation_edge: Optional[Line] = None
        names = [x for x in range(1, 1001)]
        self.node_default_names = deque(map(str, names))
        self.pre_item: Optional[GraphNode, Line] = None  # 存储地址
        self.traversal = False

    def add_node(self, position: QPoint) -> GraphNode:
        """添加新节点"""
        new_node = self.new_node(self.node_default_names.popleft())
        self.nodes[new_node.name] = new_node
        self.scene.addItem(new_node)
        position = self.mapToScene(position)
        new_node.setPos(position - QPointF(new_node.r, new_node.r))
        self.log.emit(f"created node: {new_node.name}")
        return new_node

    def new_node(self, name: str) -> GraphNode:
        res_node = GraphNode(name)
        font = QFont()
        font.setPointSize(self.font_size)
        font.setFamily(self.font_family)
        res_node.set_text_font(font)
        res_node.set_text_brush(self.font_color)
        return res_node

    def delete_item(self, delete_item: Union[GraphNode, Line]) -> None:
        if isinstance(delete_item, GraphNode):
            delete_edges = delete_item.edges
            while delete_edges:
                edge = delete_edges.pop()
                start_item = edge.start_item
                end_item = edge.end_item
                start_item.remove_edge(edge)
                end_item.remove_edge(edge)
                self.item_group.pop_item(start_item, end_item)
                self.item_group.pop_item(end_item, start_item)
                self.scene.removeItem(edge)
            self.scene.removeItem(delete_item)
            self.nodes.pop(delete_item.name)
        elif isinstance(delete_item, Line):
            start_item = delete_item.start_item
            end_item = delete_item.end_item
            start_item.remove_edge(delete_item)
            end_item.remove_edge(delete_item)
            self.item_group.pop_item(start_item, end_item)
            self.item_group.pop_item(end_item, start_item)
            self.scene.removeItem(delete_item)

    def connect_node(self, name1: str, name2: str) -> None:
        node1, node2 = self.nodes[name1], self.nodes[name2]
        if self.item_group.in_group(node1, node2):
            print("connected")
            return
        new_edge = GraphicsLineItem.new_line(node1, node2, self.edge_type)
        self.scene.addItem(new_edge)
        node1.add_edge(new_edge)
        node2.add_edge(new_edge)
        self.item_group.add_items(node1, node2)
        self.log.emit(f"connected node: {node1.name} to {node2.name}")

    def change_edge_type(self, edge_name: str) -> None:
        start_item = self.pre_item.start_item
        end_item = self.pre_item.end_item
        self.delete_item(self.pre_item)
        new_edge = GraphicsLineItem.new_line(start_item, end_item, edge_name)
        self.scene.addItem(new_edge)
        start_item.add_edge(new_edge)
        end_item.add_edge(new_edge)
        self.item_group.add_items(start_item, end_item)
        self.log.emit(f"changed line: to {edge_name}")
        self.pre_item = new_edge
        return

    def set_node_name(self, name: str) -> None:
        old_name = self.pre_item.name
        self.nodes.pop(old_name)
        self.nodes[name] = self.pre_item
        self.pre_item.name = name

    def set_line_weight(self, weight: str) -> None:
        self.pre_item.weight.setText(weight)

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        event_pos = event.position().toPoint()
        event_item = self.itemAt(event_pos)
        if event_item:
            event_item = event_item.group()
        if self.traversal:
            self.redraw()

        if self.mouse is Qt.MouseButton.LeftButton:
            # node
            if isinstance(event_item, GraphNode):
                self.clickedItem.emit(1)
                # first click
                if event_item.mode is NodeModeEnum.DEFAULT:
                    event_item.switch_mode(NodeModeEnum.SELECTED)
                # second click
                elif event_item.mode is NodeModeEnum.SELECTED:
                    event_item.switch_mode(NodeModeEnum.CREATOR)
                if isinstance(self.pre_item, GraphNode) and self.pre_item != event_item:
                    if self.pre_item.mode is NodeModeEnum.CREATOR:
                        self.connect_node(self.pre_item.name, event_item.name)
                    self.pre_item.switch_mode(NodeModeEnum.DEFAULT)
                self.pre_item = event_item
                self.nodeInfo.emit(0, event_item.name)
            # edge
            elif isinstance(event_item, Line):
                self.clickedItem.emit(0)
                if isinstance(self.pre_item, GraphNode):
                    self.pre_item.switch_mode(NodeModeEnum.DEFAULT)
                self.edgeInfo.emit(1, event_item.start_item.name, event_item.end_item.name,
                                   event_item.weight.text(), event_item.CLASS_NAME)
                self.pre_item = event_item
            # create new node
            elif event_item is None:
                # create new node and connect to pre_item
                new_node = self.add_node(event_pos)
                if isinstance(self.pre_item, GraphNode) and self.pre_item.mode is NodeModeEnum.CREATOR:
                    self.connect_node(self.pre_item.name, new_node.name)
                if isinstance(self.pre_item, GraphNode):
                    self.pre_item.switch_mode(NodeModeEnum.DEFAULT)
        elif self.mouse is Qt.MouseButton.RightButton:
            if self.pre_item and isinstance(self.pre_item, GraphNode):
                self.pre_item.switch_mode(NodeModeEnum.DEFAULT, False)
                self.pre_item = None
        self.pre_item = event_item

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mouseMoveEvent(event)
        event_pos = event.position().toPoint()
        event_pos_scene = self.mapToScene(event_pos)
        if self.mouse is Qt.MouseButton.LeftButton and isinstance(self.pre_item, GraphNode):
            self.pre_item.setPos(event_pos_scene - QPointF(self.pre_item.r, self.pre_item.r))

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(event)

    def dfs(self):
        if not isinstance(self.pre_item, GraphNode):
            return
        self.traversal = True
        self.pre_item.switch_mode(NodeModeEnum.DEFAULT)
        visited = set()
        root = self.pre_item

        def func(node: GraphNode) -> None:
            node.set_node_brush(node.SELECTED_COLOR)
            node.select_animation()
            visited.add(node)
            edges = node.edges
            for edge in edges:
                # directed edge
                if isinstance(edge, ArrowLine):
                    if edge.start_item is node and edge.end_item not in visited:
                        self.animation_edge_start(edge, True)
                        edge.traversal()
                        self.log.emit(f"traversal: {node.name} -> {edge.end_item.name}")
                        func(edge.end_item)
                # undirected edge
                else:
                    if edge.start_item is node and edge.end_item not in visited:
                        self.animation_edge_start(edge, True)
                        edge.traversal()
                        self.log.emit(f"traversal: {node.name} -> {edge.end_item.name}")
                        func(edge.end_item)
                    elif edge.end_item is node and edge.start_item not in visited:
                        self.animation_edge_start(edge)
                        edge.traversal()
                        self.log.emit(f"traversal: {node.name} -> {edge.start_item.name}")
                        func(edge.start_item)

        func(root)

    def bfs(self):
        if not isinstance(self.pre_item, GraphNode):
            return
        self.traversal = True
        self.pre_item.switch_mode(NodeModeEnum.DEFAULT)
        visited = set()
        root: GraphNode = self.pre_item
        root.switch_mode(NodeModeEnum.SELECTED)
        root.select_animation()
        visited.add(root)
        queue = [root]
        while queue:
            temp = []
            for node in queue:
                edges = node.edges
                for edge in edges:
                    # directed edge
                    if isinstance(edge, ArrowLine):
                        if edge.start_item is node and edge.end_item not in visited:
                            self.animation_edge_start(edge, True)
                            edge.traversal()
                            self.log.emit(f"traversal: {node.name} -> {edge.end_item.name}")
                            temp.append(edge.end_item)
                            edge.end_item.switch_mode(NodeModeEnum.SELECTED)
                            edge.end_item.select_animation()
                            visited.add(edge.end_item)
                    # undirected edge
                    else:
                        if edge.start_item is node and edge.end_item not in visited:
                            self.animation_edge_start(edge, True)
                            edge.traversal()
                            self.log.emit(f"traversal: {node.name} -> {edge.end_item.name}")
                            temp.append(edge.end_item)
                            edge.end_item.switch_mode(NodeModeEnum.SELECTED)
                            edge.end_item.select_animation()
                            visited.add(edge.end_item)
                        elif edge.end_item is node and edge.start_item not in visited:
                            self.animation_edge_start(edge)
                            edge.traversal()
                            self.log.emit(f"traversal: {node.name} -> {edge.start_item.name}")
                            temp.append(edge.start_item)
                            edge.start_item.switch_mode(NodeModeEnum.SELECTED)
                            edge.start_item.select_animation()
                            visited.add(edge.start_item)
            queue = temp

    def dijkstra(self):
        self.diaLog.emit("警告", "该内容暂时不开放")

    def delete(self):
        self.delete_item(self.pre_item)

    def animation_edge_start(self, edge: Optional[Line], flag=False):
        self.animation_edge = edge

        anim = QPropertyAnimation(self, b'set_line_start')
        anim.setStartValue(edge.line_end)
        anim.setEndValue(edge.line_start)
        if flag:
            anim = QPropertyAnimation(self, b'set_line_end')
            anim.setStartValue(edge.line_start)
            anim.setEndValue(edge.line_end)

        anim.setDuration(self.animation_time)
        anim.start()
        stop_time(millisecond=self.animation_time)

    @Property(QPointF)
    def set_line_end(self):
        return self.animation_edge.line_end

    @set_line_end.setter
    def set_line_end(self, p: QPointF):
        self.animation_edge.line_end = p
        if isinstance(self.animation_edge, ArrowLine):
            self.animation_edge.change_triangleItem()

    @Property(QPointF)
    def set_line_start(self):
        return self.animation_edge.line_start

    @set_line_start.setter
    def set_line_start(self, p: QPointF):
        self.animation_edge.line_start = p
        if isinstance(self.animation_edge, ArrowLine):
            self.animation_edge.change_triangleItem()

    def redraw(self):
        """redraw all the items in the scene"""
        temp = self.pre_item
        for node in self.nodes.values():
            font = QFont()
            font.setFamily(self.font_family)
            font.setPointSize(self.font_size)
            node.set_text_font(font)
            node.set_text_brush(self.font_color)
            node.set_node_brush(node.DEFAULT_COLOR)
            for edge in node.edges:
                edge.default()
                self.pre_item = edge
                self.change_edge_type(self.edge_type)
        self.pre_item = temp

    def config(self, config_dict: dict) -> None:
        global_config = config_dict["global"]
        graph_config = config_dict["graph"]
        font_color = graph_config["font_color"]
        font_size = graph_config["font_size"]
        font_family = graph_config["font_family"]
        edge_type = graph_config["edge"]
        animation_speed = global_config["animation_speed"]

        self.animation_time = animation_speed * 1000
        self.font_color = font_color
        self.font_size = font_size
        self.font_family = font_family
        self.edge_type = edge_type

        self.redraw()


class ItemGroup:
    def __init__(self):
        self.__items = defaultdict(list)

    def add_item(self, key, value) -> None:
        self.__items[key].append(value)
        self.__items[value].append(key)
        return

    def add_items(self, *args) -> None:
        for i in range(len(args)):
            item1 = args[i]
            for j in range(i + 1, len(args)):
                item2 = args[j]
                self.add_item(item1, item2)
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
            for item in items:
                if item in self.__items[key]:
                    self.__items[key].remove(item)
        elif isinstance(items, QGraphicsItem):
            if items in self.__items[key]:
                self.__items[key].remove(items)
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
    # view.delete_node("20")
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
    # view.connect_node("Name1", "Name2")
    # line = GraphicsLineItem.new_line(ZheJiang, ShangHai, LineEnum.LINE)
    # view.scene.addItem(line)

    view.show()
    sys.exit(app.exec())
