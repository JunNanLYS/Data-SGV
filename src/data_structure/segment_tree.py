from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsSimpleTextItem

from src.widgets.node_item import TextNodeItem
from src.widgets.rect_item import ClosedInterval


class SegmentTreeNode(QGraphicsItemGroup):
    def __init__(self, l: str, r: str, s: str, w=40, h=40):
        super().__init__()
        # init item
        self.node = TextNodeItem(s, w=w, h=h)
        self.interval = Interval(l, r)

        # add to group
        self.addToGroup(self.node)
        self.addToGroup(self.interval)

        # move interval
        pos = self.node.pos()
        h = self.node.boundingRect().height()
        self.interval.setPos(pos.x(), pos.y() + h)

    @property
    def sum(self) -> int:
        return int(self.node.text.text())

    @property
    def left_interval(self) -> int:
        return int(self.interval.left_text.text())

    @property
    def right_interval(self) -> int:
        return int(self.interval.right_text.text())


class Interval(QGraphicsItemGroup):
    def __init__(self, l: str, r: str):
        super().__init__()
        # init item
        self.left_interval = ClosedInterval(h=20)
        self.right_interval = ClosedInterval(h=20, direction=ClosedInterval.RIGHT)
        self.left_text = QGraphicsSimpleTextItem(l)
        self.right_text = QGraphicsSimpleTextItem(r)
        self.comma_text = QGraphicsSimpleTextItem(",")

        font = QFont()
        font.setPointSize(10)
        self.set_text_font(font)

        # add to group
        self.addToGroup(self.left_interval)
        self.addToGroup(self.right_interval)
        self.addToGroup(self.left_text)
        self.addToGroup(self.right_text)
        self.addToGroup(self.comma_text)

        # move item position
        self.__check_position()

    def set_left(self, text: str) -> None:
        self.left_text.setText(text)
        self.__check_position()

    def set_right(self, text: str) -> None:
        self.right_text.setText(text)
        self.__check_position()

    def set_text_pen(self, pen):
        self.left_text.setPen(pen)
        self.right_text.setPen(pen)
        self.comma_text.setPen(pen)

    def set_text_font(self, font):
        self.left_text.setFont(font)
        self.right_text.setFont(font)
        self.comma_text.setFont(font)

    def __check_position(self):
        w = self.left_interval.boundingRect().width()
        h = self.left_interval.boundingRect().height()
        left_text_w = self.left_text.boundingRect().width()
        text_h = self.left_text.boundingRect().height()
        right_text_w = self.right_text.boundingRect().width()
        center_h = (h / 2) - (text_h / 2)

        left_text_p = QPointF(0 + w, center_h)
        comma_text_p = QPointF(left_text_p.x() + left_text_w, center_h)
        right_text_p = QPointF(comma_text_p.x() + 5, center_h)
        right_interval_p = QPointF(right_text_p.x() + right_text_w, 0)

        self.left_text.setPos(left_text_p)
        self.comma_text.setPos(comma_text_p)
        self.right_text.setPos(right_text_p)
        self.right_interval.setPos(right_interval_p)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from src.widgets.graphics_view import MyGraphicsView

    app = QApplication()

    view = MyGraphicsView()
    item = SegmentTreeNode('1', '15', '100')
    view.scene.addItem(item)
    view.show()

    app.exec()
