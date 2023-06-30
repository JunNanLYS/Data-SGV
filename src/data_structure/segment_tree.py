from typing import Union

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsSimpleTextItem

from src.widgets.node_item import TextNodeItem
from src.widgets.rect_item import ClosedInterval


class SegmentTreeNode(QGraphicsItemGroup):
    def __init__(self, p: Union[str, int], l: Union[str, int], r: Union[str, int], s: Union[str, int], w=35, h=35):
        super().__init__()
        if isinstance(p, int):
            p = str(p)
        if isinstance(l, int):
            l = str(l)
        if isinstance(r, int):
            r = str(r)
        if isinstance(s, int):
            s = str(s)

        self.l_line = None
        self.r_line = None

        # init item
        self.setZValue(1)
        self.node = TextNodeItem(s, w=w, h=h)
        self.node.set_node_pen(Qt.NoPen)
        self.interval = Interval(p, l, r)

        # add to group
        self.addToGroup(self.node)
        self.addToGroup(self.interval)

        # move interval
        pos = self.node.pos()
        h = self.node.boundingRect().height()
        self.interval.setPos(pos.x(), pos.y() + h)

    def center(self):
        pos = self.node.pos()
        h = self.node.boundingRect().height()
        self.interval.setPos(pos.x(), pos.y() + h)

    def switch_mode(self, mode):
        self.node.switch_mode(mode)

    def boundingRect(self):
        return self.node.boundingRect()

    @property
    def sum(self) -> int:
        return int(self.node.text.text())

    @sum.setter
    def sum(self, s: Union[int, str]):
        self.node.set_text(s)

    @property
    def left_interval(self) -> int:
        return int(self.interval.left_text.text())

    @left_interval.setter
    def left_interval(self, text: Union[int, str]):
        if isinstance(text, int):
            text = str(text)
        self.interval.left_text.setText(text)
        self.interval.check_position()
        self.center()

    @property
    def right_interval(self) -> int:
        return int(self.interval.right_text.text())

    @right_interval.setter
    def right_interval(self, text: Union[int, str]):
        if isinstance(text, int):
            text = str(text)
        self.interval.right_text.setText(text)
        self.interval.check_position()
        self.center()


class Interval(QGraphicsItemGroup):
    def __init__(self, p: str, l: str, r: str):
        super().__init__()
        # init item
        self.hidden = False
        self.left_interval = ClosedInterval(h=15)
        self.right_interval = ClosedInterval(h=15, direction=ClosedInterval.RIGHT)
        self.p_text = QGraphicsSimpleTextItem(p + " : ")
        self.left_text = QGraphicsSimpleTextItem(l)
        self.right_text = QGraphicsSimpleTextItem(r)
        self.comma_text = QGraphicsSimpleTextItem(",")

        font = QFont()
        font.setPointSize(8)
        self.set_text_font(font)

        # add to group
        self.addToGroup(self.left_interval)
        self.addToGroup(self.right_interval)
        self.addToGroup(self.p_text)
        self.addToGroup(self.left_text)
        self.addToGroup(self.right_text)
        self.addToGroup(self.comma_text)

        # move item position
        self.check_position()

    def set_left(self, text: str) -> None:
        self.left_text.setText(text)
        self.check_position()

    def set_right(self, text: str) -> None:
        self.right_text.setText(text)
        self.check_position()

    def set_text_pen(self, pen):
        self.left_text.setPen(pen)
        self.right_text.setPen(pen)
        self.comma_text.setPen(pen)

    def set_text_font(self, font):
        self.p_text.setFont(font)
        self.left_text.setFont(font)
        self.right_text.setFont(font)
        self.comma_text.setFont(font)

    def check_position(self):
        w = self.left_interval.boundingRect().width()
        h = self.left_interval.boundingRect().height()
        left_text_w = self.left_text.boundingRect().width()
        text_h = self.left_text.boundingRect().height()
        right_text_w = self.right_text.boundingRect().width()
        center_h = (h / 2) - (text_h / 2)

        p_text_p = QPointF(0 - self.p_text.boundingRect().width(), center_h)
        left_text_p = QPointF(0 + w, center_h)
        comma_text_p = QPointF(left_text_p.x() + left_text_w, center_h)
        right_text_p = QPointF(comma_text_p.x() + 5, center_h)
        right_interval_p = QPointF(right_text_p.x() + right_text_w, 0)

        self.p_text.setPos(p_text_p)
        self.left_text.setPos(left_text_p)
        self.comma_text.setPos(comma_text_p)
        self.right_text.setPos(right_text_p)
        self.right_interval.setPos(right_interval_p)

    def is_hidden(self):
        return self.hidden

    def show(self) -> None:
        super().show()
        self.hidden = False

    def hide(self) -> None:
        super().hide()
        self.hidden = True


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from src.widgets.graphics_view import MyGraphicsView

    app = QApplication()

    view = MyGraphicsView()
    item = SegmentTreeNode('1', '15', '100', '100')
    view.scene.addItem(item)
    view.show()

    app.exec()
