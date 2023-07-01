import PySide6
from PySide6 import QtCore
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QMainWindow, QWidget

from functools import singledispatchmethod

from qfluentwidgets import PixmapLabel


class ImageWidget(PixmapLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(PySide6.QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(PySide6.QtCore.Qt.FramelessWindowHint)
        self.leave_hide = True
        self.click = True
        self.default_image = None

        self.new_widget = None

    def image(self) -> QPixmap:
        return self.pixmap()

    def set_image(self, pixmap: QPixmap, default=True) -> None:
        """
        default is True change default_image
        default is False not change default_image
        """
        if default:
            self.default_image = pixmap
        self.setPixmap(pixmap)

    def set_leave_hide(self, switch: bool) -> None:
        self.leave_hide = switch

    def set_click(self, switch: bool):
        self.click = switch

    def scaled(self, w: int, h: int, aspectMode: Qt.AspectRatioMode, mode: Qt.TransformationMode) -> None:
        pixmap = self.default_image
        pixmap = pixmap.scaled(w, h, aspectMode, mode)
        self.set_image(pixmap, False)

    def leaveEvent(self, event: PySide6.QtCore.QEvent) -> None:
        if self.leave_hide:
            self.hide()

    def mousePressEvent(self, ev: PySide6.QtGui.QMouseEvent) -> None:
        if not self.click:
            return

        new_image = ImageWidget()
        new_image.set_image(self.default_image)
        new_image.scaled(1000,
                         800,
                         Qt.AspectRatioMode.KeepAspectRatio,
                         Qt.TransformationMode.SmoothTransformation)
        new_image.set_leave_hide(False)
        new_image.set_click(False)
        self.new_widget = ImageViewer(new_image)
        new_image.setParent(self.new_widget)
        self.new_widget.resize(new_image.width(), new_image.height())
        self.new_widget.show()


class ImageViewer(QWidget):
    @singledispatchmethod
    def __init__(self, image_w: ImageWidget, parent: QWidget = None):
        super().__init__(parent)
        self.image_widget = image_w

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        new_width = event.size().width()
        new_height = event.size().height()
        self.image_widget.scaled(new_width, new_height,
                                 Qt.AspectRatioMode.IgnoreAspectRatio,
                                 Qt.TransformationMode.SmoothTransformation)
