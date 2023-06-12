from PySide6.QtCore import QLineF
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsRectItem


class SquareItem(QGraphicsRectItem):
    DEFAULT_COLOR = QColor(204, 255, 255)  # blue

    def __init__(self, w: int = 50, h: int = 50, parent=None):
        super().__init__(0, 0, w, h, parent)
        self.setBrush(self.DEFAULT_COLOR)


class ClosedInterval(QGraphicsRectItem):
    DEFAULT_COLOR = QColor(0, 0, 0)
    LEFT = 0
    RIGHT = 1

    def __init__(self, w: int = 5, h: int = 30, direction: int = 0, parent=None):
        super().__init__(0, 0, w, h, parent)
        self.setPen(QPen(self.DEFAULT_COLOR, 1.5))
        self.direction = direction  # 0 is left, 1 is right

    def set_direction(self, direction: int):
        """direction is 0 or 1"""
        if direction in [self.LEFT, self.RIGHT]:
            self.direction = direction
        else:
            raise AttributeError("direction must is 0 or 1")

    def paint(self, painter, option, widget=...) -> None:
        painter.setPen(self.pen())
        rect = self.rect()
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        line1 = QLineF(x, y, x + w, y)
        line2 = QLineF(x, y + h, x + w, y + h)
        if self.direction == 0:
            line3 = QLineF(x, y, x, y + h)
        else:
            line3 = QLineF(x + w, y, x + w, y + h)

        painter.drawLines([line1, line2, line3])


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from src.widgets.graphics_view import MyGraphicsView

    app = QApplication()

    view = MyGraphicsView()
    view.resize(500, 500)
    item = ClosedInterval(10, 30)
    item.setPos(100, 100)
    view.scene.addItem(item)
    view.show()

    app.exec()
