# Python library
import time
from collections import deque

# MyStruct
# Qt
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QCursor, QBrush, QColor, QPen
from PySide6.QtCore import Qt, QPointF, QTimeLine, QTime, QCoreApplication, QEventLoop, QPoint, Property, \
    QPropertyAnimation
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItemAnimation

from src.View.GraphItems import GraphEllipseItem, GraphArrowLine


def stopTime(second: int):
    endTime = QTime.currentTime().addSecs(second)
    while QTime.currentTime() < endTime:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)


class GraphView(QGraphicsView):
    __mouse = Qt.MouseButton.NoButton  # 记录点击事件，用来传递给移动事件

    preItem = None  # 上一个item
    preLine = None
    _enlarge = 0  # 放大的次数
    _shrink = 0  # 缩小的次数

    lastPos = QtCore.QPointF()  # 作用 -> 记录鼠标位置，移动view

    def __init__(self, parent: QtWidgets = None):
        super(GraphView, self).__init__(parent)
        self.selectNode = False
        self.__select = []
        self._color = QColor(255, 255, 255)

        # setting
        if not self.isInteractive(): print("MyGraphicsView: 没有开启场景交互功能")  # 判断有没有进行场景交互
        self.setScene(QGraphicsScene(self.x(), self.y(), self.width(), self.height(), self))  # 内置一个场景
        self.viewport().setProperty("cursor", QCursor(Qt.CrossCursor))  # 设置光标为十字型  ( + )

    # 鼠标点击
    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())  # 获取点击位置的item
        self.__mouse = event.button()  # 记录鼠标事件

        # 线条
        if item and type(item) == GraphArrowLine:
            if event.button() == Qt.MouseButton.LeftButton:
                item.reversed()
            elif event.button() == Qt.MouseButton.RightButton:
                self.preLine = item
                item.delete()
                self.arrowLine_deleted_animation()
                stopTime(1)
                self.scene().removeItem(item)
            else:
                return

        # 鼠标中间
        if event.button() == Qt.MiddleButton:
            self.lastPos = self.mapToScene(event.pos())
            return

        # 节点
        if item and type(item) == GraphEllipseItem:
            # 左键移动节点 -> item处理
            if event.button() == Qt.LeftButton:
                # 没有被选中的节点
                if not self.selectNode:
                    item.select_color()  # 颜色
                    self.preItem = item
                    self.selectNode = True
                    QGraphicsView.mousePressEvent(self, event)
                    return
                # 已经有选中的节点
                elif self.selectNode:
                    if self.preItem == item:
                        item.unselect()  # 颜色
                        self.selectNode = False
                        QGraphicsView.mousePressEvent(self, event)
                        return
                    # 连接节点
                    else:
                        start, end = self.preItem, item
                        start.unselect()  # 颜色 | 取消选中
                        line = GraphArrowLine(start, end)  # 线条
                        self.preLine = line
                        self.scene().addItem(line)
                        # 启动动画并连接
                        # self.arrowLine_connecting_animation()
                        self.selectNode = False
                        # stopTime(1)

                        # 保存数据
                        start.moveLine.append(line)
                        start.next.append(line)
                        start.line[end] = line
                        end.moveLine.append(line)
                        return
            # 右键删除节点
            elif event.button() == Qt.RightButton:
                self.selectNode = False
                if self.preItem: self.preItem.unselect()
                item.delete_animation()  # 动画
                # 与右键的节点有关的所有线条删除
                for line in item.moveLine:
                    self.scene().removeItem(line)
                stopTime(1)  # 非阻塞延迟1秒
                self.scene().removeItem(item)
                return
        # item is None
        elif item is None:
            # 左键创建节点
            if event.button() == Qt.LeftButton:
                self.selectNode = False
                if self.preItem is not None: self.preItem.unselect()  # 上一个item取消选择
                newItem = GraphEllipseItem()  # 新节点
                self.scene().addItem(newItem)  # 新节点加入scene
                r = QPoint(newItem.boundingRect().center().x(), newItem.boundingRect().center().y())  # 获取半径
                point = self.mapToScene(event.pos() - r)  # 坐标矫正
                newItem.setPos(point)  # 修改坐标
                newItem.creat_animation()  # 动画
                self.preItem = newItem
                return

    # 鼠标移动
    def mouseMoveEvent(self, event) -> None:
        # 移动view
        if self.__mouse == Qt.MiddleButton:
            dp = self.mapToScene(event.pos()) - self.lastPos
            sRect = self.sceneRect()
            self.setSceneRect(sRect.x() - dp.x(), sRect.y() - dp.y(), sRect.width(), sRect.height())
            self.lastPos = self.mapToScene(event.pos())
            return
        QGraphicsView.mouseMoveEvent(self, event)

    # 鼠标释放
    def mouseReleaseEvent(self, event) -> None:
        QGraphicsView.mouseReleaseEvent(self, event)
        self.__mouse = Qt.MouseButton.NoButton
        # print("View: 鼠标释放")

    # 滚轮
    def wheelEvent(self, event) -> None:
        # ----------------------------------------------------------------
        # 等比例缩放
        wheelValue = event.angleDelta().y()
        ratio = wheelValue / 1200 + 1  # ratio -> 1.1 or 0.9
        if ratio > 1:  # 放大次数6
            if self._enlarge < 6:
                self._enlarge += 1
                self._shrink -= 1
                self.scale(ratio, ratio)
        else:  # 缩小次数5
            if self._shrink < 5:
                self._shrink += 1
                self._enlarge -= 1
                self.scale(ratio, ratio)
        # ----------------------------------------------------------------

    # 深度优先遍历(Deep first search)
    def dfs(self, root: GraphEllipseItem, s=None):
        if s is None: s = set()
        if root is None:
            return
        next_nodes = root.line.keys()
        root.select_color()  # 颜色
        root.select_animation()
        self.__select.append(root)
        s.add(root)
        for node in next_nodes:
            if node not in s:
                self.preLine = root.line[node]
                self.arrowLine_connecting_animation()
                stopTime(1)
                self.dfs(node, s)

    # 广度优先遍历(Breadth first search)
    def bfs(self, root: GraphEllipseItem, s=None):
        if s is None: s = set()
        if root is None: return
        root.select_color()
        root.select_animation()
        self.__select.append(root)
        s.add(root)
        node = [root.line]
        while node:
            temp = []
            for nodes in node:
                for k, v in nodes.items():
                    if k not in s:
                        s.add(k)
                        self.preLine = v
                        self.arrowLine_connecting_animation()
                        stopTime(1)
                        k.select_color()
                        k.select_animation()
                        self.__select.append(k)
                        temp.append(k.line)
            node = temp

    # -----------------------------------------
    # 线条连接动画
    @Property(QPointF)
    def connecting_line(self):
        return self.preLine.end

    @connecting_line.setter
    def connecting_line(self, p):
        self.preLine.end = p
        self.preLine.create_path()

    # 连接动画
    def arrowLine_connecting_animation(self):
        anim = QPropertyAnimation(self)
        anim.setTargetObject(self)
        anim.setPropertyName(b'connecting_line')
        anim.setStartValue(self.preLine.start)
        anim.setEndValue(self.preLine.end)
        anim.setDuration(500)
        anim.start()

    # 删除动画
    def arrowLine_deleted_animation(self):
        anim = QPropertyAnimation(self)
        anim.setTargetObject(self)
        anim.setPropertyName(b'connecting_line')
        # 从终点移动到起点
        anim.setStartValue(self.preLine.end)
        anim.setEndValue(self.preLine.start)
        anim.setDuration(500)
        anim.start()

    # -----------------------------------------

    # 遍历完成后对所有节点颜色改回来
    def all_unselect(self):
        for node in self.__select:
            node.unselect()
        self.__select = []

    def __str__(self):
        return "这里是自定义视图"
