from functools import singledispatchmethod

from PySide6.QtCore import Signal, QPoint
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QWidget
from qfluentwidgets import PushButton

from src.widgets.image import ImageWidget


class PixmapButton(PushButton):
    enter = Signal()
    leave = Signal()
    imageShow = Signal()
    imageHide = Signal()

    @singledispatchmethod
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_width = 100
        self.image_height = 100
        self.image_widget = ImageWidget()

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

    def set_image_size(self, w: int, h: int):
        self.image_width = w
        self.image_height = h

    def enterEvent(self, e):
        self.enter.emit()

    def leaveEvent(self, e):
        cursor_pos = self.mapToGlobal(self.mapFromGlobal(self.cursor().pos()))
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
        self.image_widget.scaled(self.image_width,
                                 self.image_height,
                                 Qt.AspectRatioMode.IgnoreAspectRatio,
                                 Qt.TransformationMode.SmoothTransformation)

        pos = self.mapToGlobal(self.mapFromParent(self.pos()))
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
