from typing import Optional

import PySide6
from PySide6 import QtCore
from PySide6.QtCore import QPoint, Qt, QEvent, Signal, QSize
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect


class DefaultWidget(QWidget):
    brush = QBrush(QColor(250, 250, 250))

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)

    def set_widget_brush(self, brush: QBrush) -> None:
        """修改Widget背景颜色"""
        self.brush = brush
        self.update()

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(self.rect(), 10, 10)


class MaskWidget(DefaultWidget):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_widget_brush(Qt.black)
        self.move(self.parent().pos())
        self.resize(parent.width(), parent.height())
        self.hide()

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.clicked.emit()
        return

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.gray)
        painter.setOpacity(0.8)  # 设置透明度
        painter.drawRoundedRect(self.rect(), 10, 10)

    def update_size(self):
        width = self.parent().width()
        height = self.parent().height()
        self.resize(width, height)


class RoundedWidget(DefaultWidget):
    mouse = Qt.MouseButton.NoButton
    last_position = QPoint()
    pre_window = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(QSize(1000, 800))
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.setMouseTracking(True)
        self.installEventFilter(self)

        self.border = MousePosition(self)
        self.top_vertical, self.lower_vertical = False, False
        self.left_horizontal, self.right_horizontal = False, False
        self.top_left_diag, self.top_right_diag = False, False
        self.lower_left_diag, self.lower_right_diag = False, False
        self.filter_state = True

    def eventFilter(self, watched: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent) -> bool:
        """返回False不拦截事件，返回True则拦截事件下面的widget以及一些函数无法接收到event"""

        if not self.filter_state:
            return False

        def default() -> None:
            """将实例属性全部设置为False,方便后面设置"""
            self.top_vertical, self.lower_vertical = False, False
            self.left_horizontal, self.right_horizontal = False, False
            self.top_left_diag, self.top_right_diag = False, False
            self.lower_left_diag, self.lower_right_diag = False, False

        # 监听widget的鼠标移动
        if watched is self and event.type() is QEvent.MouseMove:
            event_pos = event.position().toPoint()
            # 水平拉伸
            if self.border.is_left_border(event_pos) or self.border.is_right_border(event_pos):
                # return False
                default()
                self.setCursor(Qt.SizeHorCursor)
                if self.border.is_left_border(event_pos):
                    self.left_horizontal = True
                else:
                    self.right_horizontal = True
            # 垂直拉伸
            elif self.border.is_top_border(event_pos) or self.border.is_lower_border(event_pos):
                default()
                self.setCursor(Qt.SizeVerCursor)
                if self.border.is_top_border(event_pos):
                    self.top_vertical = True
                else:
                    self.lower_vertical = True
            # 反斜
            elif self.border.is_top_left(event_pos) or self.border.is_lower_right(event_pos):
                default()
                self.setCursor(Qt.SizeFDiagCursor)
                if self.border.is_top_left(event_pos):
                    self.top_left_diag = True
                else:
                    self.lower_right_diag = True
            # 正斜
            elif self.border.is_top_right(event_pos) or self.border.is_lower_left(event_pos):
                default()
                self.setCursor(Qt.SizeBDiagCursor)
                if self.border.is_top_right(event_pos):
                    self.top_right_diag = True
                else:
                    self.lower_left_diag = True
            # 恢复
            else:
                default()
                self.setCursor(Qt.ArrowCursor)
        return False

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.border.update()

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = event.button()
        event_pos = event.position()
        if self.mouse == Qt.MouseButton.LeftButton:
            self.last_position = event_pos.toPoint()
        event.accept()

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        event_pos = event.position()
        if self.mouse == Qt.MouseButton.LeftButton:
            self.filter_state = False
            # 横向伸缩
            if self.left_horizontal or self.right_horizontal:
                if self.left_horizontal:
                    x = abs(event_pos.x() - self.width() - 10)
                    diff = x - self.width()
                    if x < self.minimumWidth():
                        return
                    self.setGeometry(self.x() - diff, self.y(), x, self.height())
                else:
                    self.resize(event_pos.x() + 10, self.height())
            # 垂直伸缩
            elif self.top_vertical or self.lower_vertical:
                if self.top_vertical:
                    y = abs(event_pos.y() - self.height() - 10)
                    diff = y - self.height()
                    if y < self.minimumHeight():
                        return
                    self.setGeometry(self.x(), self.y() - diff, self.width(), y)
                elif self.lower_vertical:
                    self.resize(self.width(), event_pos.y() + 10)
            # 左上和右下伸缩
            elif self.top_left_diag or self.lower_right_diag:
                if self.top_left_diag:
                    x = abs(event_pos.x() - self.width() - 10)
                    y = abs(event_pos.y() - self.height() - 10)
                    diff_x = x - self.width()
                    diff_y = y - self.height()
                    if x < self.minimumWidth() or y < self.minimumHeight():
                        return
                    self.setGeometry(self.x() - diff_x, self.y() - diff_y, x, y)
                else:
                    self.resize(event_pos.x() + 10, event_pos.y() + 10)
            # 右上和左下伸缩
            elif self.top_right_diag or self.lower_left_diag:
                if self.top_right_diag:
                    y = abs(event_pos.y() - self.height() - 10)
                    diff = y - self.height()
                    if y < self.minimumHeight():
                        return
                    self.setGeometry(self.x(), self.y() - diff, event_pos.x() + 10, y)
                else:
                    x = abs(event_pos.x() - self.width() - 10)
                    diff = x - self.width()
                    if x < self.minimumWidth():
                        return
                    self.setGeometry(self.x() - diff, self.y(), x, event_pos.y() + 10)
            else:
                self.move(self.mapToGlobal(event_pos.toPoint()) - self.last_position)
        event.accept()

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = Qt.MouseButton.NoButton
        self.filter_state = True


class RoundedWindow(RoundedWidget):
    sizeChanged = Signal(int, int)
    maskShow = Signal()
    maskHide = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # init mask
        self.__mask = MaskWidget(self)
        self.__mask.clicked.connect(self.hide_mask)

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.sizeChanged.emit(self.width(), self.height())
        self.__mask.update_size()

    def show_mask(self):
        self.__mask.raise_()
        self.__mask.show()
        self.maskShow.emit()

    def hide_mask(self):
        self.__mask.hide()
        self.maskHide.emit()


class ShadowWindow(DefaultWidget):
    sizeChanged = Signal(int, int)
    maskShow = Signal()
    maskHide = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self._background = BackGround(self)
        self._isResizeEnabled = True
        self.mouse = Qt.NoButton
        self.last_pos = QPoint(0, 0)

        self.resize(QSize(1000, 800))

        self.set_widget_brush(QColor(0, 0, 0, 360))

        # init background
        radius = self.background().shadow_radius
        self.resize(QSize(self.width(), self.height()))
        self.background().move(radius, radius)
        self.setMinimumSize(QSize(200, 200))

        # init mask
        self._mask = MaskWidget(self)
        self._mask.clicked.connect(self.hide_mask)

        # init Qt.Edge dict
        self.edge_to_obj = {Qt.LeftEdge: False,
                            Qt.RightEdge: False,
                            Qt.TopEdge: False,
                            Qt.BottomEdge: False,
                            Qt.LeftEdge | Qt.TopEdge: False,
                            Qt.RightEdge | Qt.TopEdge: False,
                            Qt.LeftEdge | Qt.BottomEdge: False,
                            Qt.RightEdge | Qt.BottomEdge: False, }

    def show_mask(self):
        self._mask.raise_()
        self._mask.show()
        self.maskShow.emit()

    def hide_mask(self):
        self._mask.hide()
        self.maskHide.emit()

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.sizeChanged.emit(self.width(), self.height())
        self._mask.update_size()

    def eventFilter(self, watched: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent) -> bool:
        et = event.type()
        if et != QEvent.MouseMove or not self._isResizeEnabled:
            return False

        edges = Qt.Edge(0)
        pos = event.globalPosition().toPoint() - self.pos()
        if 0 <= pos.x() < self._background.PADDING:
            edges |= Qt.LeftEdge
        if self.width() >= pos.x() >= self.width() - self._background.PADDING:
            edges |= Qt.RightEdge
        if 0 <= pos.y() < self._background.PADDING:
            edges |= Qt.TopEdge
        if self.height() >= pos.y() >= self.height() - self._background.PADDING:
            edges |= Qt.BottomEdge

        # change cursor style
        if et == QEvent.MouseMove and self.windowState() == Qt.WindowNoState:
            if edges in (Qt.LeftEdge | Qt.TopEdge, Qt.RightEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeFDiagCursor)
            elif edges in (Qt.RightEdge | Qt.TopEdge, Qt.LeftEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeBDiagCursor)
            elif edges in (Qt.TopEdge, Qt.BottomEdge):
                self.setCursor(Qt.SizeVerCursor)
            elif edges in (Qt.LeftEdge, Qt.RightEdge):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        return False

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = event.button()
        self.last_pos = event.position().toPoint()
        edges = Qt.Edge(0)
        pos = event.globalPosition().toPoint() - self.pos()
        if 0 <= pos.x() < self._background.PADDING:
            edges |= Qt.LeftEdge
        if self.width() >= pos.x() >= self.width() - self._background.PADDING:
            edges |= Qt.RightEdge
        if 0 <= pos.y() < self._background.PADDING:
            edges |= Qt.TopEdge
        if self.height() >= pos.y() >= self.height() - self._background.PADDING:
            edges |= Qt.BottomEdge

        self.edge_to_obj[edges] = True

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        event_pos = event.position()

        # resize
        if self.mouse == Qt.MouseButton.LeftButton:
            if True in self.edge_to_obj.values() and self._isResizeEnabled:
                radius = self._background.shadow_radius
                width = self.width() + radius * 2
                height = self.height() + radius * 2
                x = abs(event_pos.x() - width - 10)
                y = abs(event_pos.y() - height - 10)
                diff_x = x - width
                diff_y = y - height
                # 横向伸缩
                # 左边界
                if self.edge_to_obj[Qt.LeftEdge]:
                    if x < self.minimumWidth():
                        return
                    self.move(self.x() - diff_x, self.y())
                    self.resize(QSize(x, height))
                # 右边界
                elif self.edge_to_obj[Qt.RightEdge]:
                    self.resize(QSize(event_pos.x() + 15, height))
                # 垂直伸缩
                elif self.edge_to_obj[Qt.TopEdge]:
                    if y < self.minimumHeight():
                        return
                    self.move(self.x(), self.y() - diff_y)
                    self.resize(QSize(width, y))
                elif self.edge_to_obj[Qt.BottomEdge]:
                    self.resize(QSize(width, event_pos.y() + 15))
                # 左上和右下伸缩
                elif self.edge_to_obj[Qt.LeftEdge | Qt.TopEdge]:
                    if x < self.minimumWidth() or y < self.minimumHeight():
                        return
                    self.move(self.x() - diff_x, self.y() - diff_y)
                    self.resize(QSize(x, y))
                elif self.edge_to_obj[Qt.RightEdge | Qt.BottomEdge]:
                    self.resize(QSize(event_pos.x() + 15, event_pos.y() + 15))
                # 右上和左下伸缩
                elif self.edge_to_obj[Qt.RightEdge | Qt.TopEdge]:
                    if y < self.minimumHeight():
                        return
                    self.move(self.x(), self.y() - diff_y)
                    self.resize(QSize(event_pos.x() + 15, y))
                elif self.edge_to_obj[Qt.LeftEdge | Qt.BottomEdge]:
                    if x < self.minimumWidth():
                        return
                    self.move(self.x() - diff_x, self.y())
                    self.resize(QSize(x, event_pos.y() + 15))
                else:
                    self.move(self.mapToGlobal(event_pos.toPoint()) - self.last_pos)
        else:
            event.accept()

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = Qt.NoButton
        for v in self.edge_to_obj.keys():
            self.edge_to_obj[v] = False

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled

    def background(self):
        return self._background

    def set_child_parent(self):
        for child in self.children():
            if child is self._background:
                continue
            child.setParent(self._background)

    def width(self) -> int:
        return self._background.width()

    def height(self) -> int:
        return self._background.height()

    def setMinimumSize(self, size: PySide6.QtCore.QSize) -> None:
        super().setMinimumSize(size)
        radius = self._background.shadow_radius
        new_size = size - QSize(radius * 2, radius * 2)
        self._background.setMinimumSize(QSize(new_size))

    def resize(self, new_size: PySide6.QtCore.QSize) -> None:
        super().resize(new_size)
        radius = self.background().shadow_radius
        size = QSize(radius * 2, radius * 2)
        self.background().resize(new_size - size)

    def pos(self) -> PySide6.QtCore.QPoint:
        radius = self.background().shadow_radius
        point = QPoint(radius, radius)
        return super().pos() + point


class BackGround(DefaultWidget):
    PADDING = 10

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.shadow_radius = 10

        # init shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QColor(0, 0, 0))
        self.shadow.setBlurRadius(self.shadow_radius)
        self.setGraphicsEffect(self.shadow)

        # self.show()

    def set_shadow_radius(self, radius: int):
        self.shadow_radius = radius
        self.shadow.setBlurRadius(radius)


class MousePosition:
    def __init__(self, widget: QWidget, size: int = 10):
        self.widget = widget
        self.size = size
        self.top_left = [QPoint(0, 0), QPoint(size, 0),
                         QPoint(0, size), QPoint(size, size)]
        self.top_right = [QPoint(self.width - size, 0), QPoint(self.width, 0),
                          QPoint(self.width - size, size), QPoint(self.width, size)]
        self.lower_left = [QPoint(0, self.height - size), QPoint(size, self.height - size),
                           QPoint(0, self.height), QPoint(size, self.height)]
        self.lower_right = [QPoint(self.width - size, self.height - size), QPoint(self.width, self.height - size),
                            QPoint(self.width - size, self.height), QPoint(self.width, self.height)]

        self.left_border = [QPoint(0, size), QPoint(size, size),
                            QPoint(0, self.height - size), QPoint(size, self.height - size)]
        self.right_border = [QPoint(self.width - size, size), QPoint(self.width, size),
                             QPoint(self.width - size, self.height - size), QPoint(self.width, self.height - size)]
        self.top_border = [QPoint(size, 0), QPoint(self.width - size, 0),
                           QPoint(size, size), QPoint(self.width - size, size)]
        self.lower_border = [QPoint(size, self.height - size), QPoint(self.width - size, self.height - size),
                             QPoint(size, self.height), QPoint(self.width - size, self.height)]

    def is_top_left(self, position: QPoint) -> bool:
        return judge(position, self.top_left)

    def is_top_right(self, position: QPoint) -> bool:
        return judge(position, self.top_right)

    def is_lower_left(self, position: QPoint) -> bool:
        return judge(position, self.lower_left)

    def is_lower_right(self, position: QPoint) -> bool:
        return judge(position, self.lower_right)

    def is_left_border(self, position: QPoint) -> bool:
        return judge(position, self.left_border)

    def is_right_border(self, position: QPoint) -> bool:
        return judge(position, self.right_border)

    def is_top_border(self, position: QPoint) -> bool:
        return judge(position, self.top_border)

    def is_lower_border(self, position: QPoint) -> bool:
        return judge(position, self.lower_border)

    def is_border(self, position: QPoint) -> bool:
        """判断是否处于边界"""
        return self.is_top_left(position) \
            or self.is_top_right(position) \
            or self.is_lower_left(position) \
            or self.is_lower_right(position) \
            or self.is_left_border(position) \
            or self.is_right_border(position) \
            or self.is_top_border(position) \
            or self.is_lower_border(position)

    def update(self):
        size = self.size
        self.top_left = [QPoint(0, 0), QPoint(size, 0),
                         QPoint(0, size), QPoint(size, size)]
        self.top_right = [QPoint(self.width - size, 0), QPoint(self.width, 0),
                          QPoint(self.width - size, size), QPoint(self.width, size)]
        self.lower_left = [QPoint(0, self.height - size), QPoint(size, self.height - size),
                           QPoint(0, self.height), QPoint(size, self.height)]
        self.lower_right = [QPoint(self.width - size, self.height - size), QPoint(self.width, self.height - size),
                            QPoint(self.width - size, self.height), QPoint(self.width, self.height)]

        self.left_border = [QPoint(0, size), QPoint(size, size),
                            QPoint(0, self.height - size), QPoint(size, self.height - size)]
        self.right_border = [QPoint(self.width - size, size), QPoint(self.width, size),
                             QPoint(self.width - size, self.height - size), QPoint(self.width, self.height - size)]
        self.top_border = [QPoint(size, 0), QPoint(self.width - size, 0),
                           QPoint(size, size), QPoint(self.width - size, size)]
        self.lower_border = [QPoint(size, self.height - size), QPoint(self.width - size, self.height - size),
                             QPoint(size, self.height), QPoint(self.width - size, self.height)]

    @property
    def width(self):
        return self.widget.width()

    @property
    def height(self):
        return self.widget.height()


# 辅助函数
def judge(position: QPoint, position_array: list[QPoint]) -> bool:
    x1, y1 = position_array[0].x(), position_array[0].y()
    x2, y2 = position_array[3].x(), position_array[3].y()
    if x1 <= position.x() <= x2 and y1 <= position.y() <= y2:
        return True
    return False


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = RoundedWindow()
    window.show_mask()
    window.show()
    sys.exit(app.exec())
