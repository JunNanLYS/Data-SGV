from PySide6.QtGui import QPixmap, Qt, QMouseEvent, QCursor
from PySide6.QtCore import Signal, QPoint
from PySide6.QtWidgets import QWidget

from qfluentwidgets import PushButton, PixmapLabel

from functools import singledispatchmethod

from src.widgets.image import ImageWidget


class PixmapButton(PushButton):
    enter = Signal()
    leave = Signal()
    imageShow = Signal()
    imageHide = Signal()

    @singledispatchmethod
    def __init__(self, parent=None):
        super().__init__(parent)
        self._factor = 3
        self.image_widget = ImageWidget(self.parent())

        # signal connect slot
        self.enter.connect(self.__show_pixmap)
        self.leave.connect(self.__hide_pixmap)

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)

    def set_image(self, image: QPixmap):
        self.image_widget.set_image(image)
        self.image_widget.hide()

    def enterEvent(self, e):
        self.enter.emit()

    def leaveEvent(self, e):
        cursor_pos = self.mapToParent(self.mapFromGlobal(self.cursor().pos()))
        cursor_x = cursor_pos.x()
        cursor_y = cursor_pos.y()
        image_pos = self.image_widget.pos()
        image_x = image_pos.x()
        image_y = image_pos.y()
        if image_x <= cursor_x <= image_x + self.image_widget.width() \
                and image_y <= cursor_y <= image_y + self.image_widget.height():
            pass
        else:
            self.leave.emit()

    def __center_up_image(self):
        self.image_widget.scaled(self.width() * self.factor,
                                 self.height() * self.factor,
                                 Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                 Qt.TransformationMode.SmoothTransformation)

        pos = self.pos()
        pos += QPoint(self.width() // 2, 0)
        pos -= QPoint(self.image_widget.width() // 2, self.image_widget.height())
        self.image_widget.move(pos)

    def __show_pixmap(self):
        self.__center_up_image()
        self.image_widget.show()

        self.imageShow.emit()

    def __hide_pixmap(self):
        self.image_widget.hide()

        self.imageHide.emit()

    @property
    def factor(self):
        return self._factor

    @factor.setter
    def factor(self, num):
        self._factor = num
        self.__center_up_image()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication()

    window = QMainWindow()
    window.resize(1000, 800)

    button = PixmapButton("Binary Tree", window)
    button.move(400, 400)
    pix = QPixmap("../../images/graph.png")
    button.set_image(pix)
    button.factor = 1

    window.show()

    app.exec()
