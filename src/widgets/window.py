import math
from typing import Union, Optional

import PySide6
from PySide6.QtCore import QSize, QEvent, Qt, Signal, QPoint
from PySide6.QtGui import QColor, QPainter, QBrush

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QLayout, QVBoxLayout
from qframelesswindow import SvgTitleBarButton, FramelessWindow
from qfluentwidgets import ToolButton, FluentIcon, PushButton, NavigationPanel, NavigationBar, \
    NavigationWidget

from src.auxiliary_function import layout_add_bojs, layout_add_obj
from src.tool import PathTool


class DefaultWidget(QWidget):
    sizeChanged = Signal(QSize)
    maskShow = Signal()
    maskHide = Signal()
    brush = QBrush(QColor(255, 255, 255))

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._isResizeEnabled = True

    def set_widget_brush(self, brush: QBrush) -> None:
        """修改Widget背景颜色"""
        self.brush = brush
        self.update()

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        self.sizeChanged.emit(event.size())

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(self.rect(), 10, 10)

    def setResizeEnabled(self, isEnabled: bool):
        """ set whether resizing is enabled """
        self._isResizeEnabled = isEnabled


class Mask(DefaultWidget):
    def __init__(self, parent: DefaultWidget):
        super().__init__(parent)
        self.set_widget_brush(QColor(63, 63, 63, 180))
        self.hide()

        # connect signal to slot
        self.parent().sizeChanged.connect(self.resize)
        self.parent().maskShow.connect(self.show)
        self.parent().maskShow.connect(self.raise_)
        self.parent().maskHide.connect(self.hide)

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        """transmit signal to parent widget and hide mask"""
        self.hide()
        self.parent().maskHide.emit()
        event.accept()


class RoundWindow(DefaultWidget):
    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.brush = QColor(245, 245, 245)
        self._isResizeEnabled = True
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        et = event.type()
        if et != QEvent.MouseButtonPress and et != QEvent.MouseMove or not self._isResizeEnabled:
            return False

        edges = Qt.Edge(0)
        pos = event.globalPosition() - self.pos()
        if pos.x() < self.BORDER_WIDTH:
            edges |= Qt.LeftEdge
        if pos.x() >= self.width() - self.BORDER_WIDTH:
            edges |= Qt.RightEdge
        if pos.y() < self.BORDER_WIDTH:
            edges |= Qt.TopEdge
        if pos.y() >= self.height() - self.BORDER_WIDTH:
            edges |= Qt.BottomEdge

        # change cursor
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

        elif obj is self and et == QEvent.MouseButtonPress and edges:
            self.windowHandle().startSystemResize(edges)

        return False

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.windowHandle().startSystemMove()


class TitleBar(DefaultWidget):
    def __init__(self, parent: DefaultWidget):
        super().__init__(parent)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        self._isDoubleClickEnabled = True
        self.setFixedHeight(50)
        self._layout_main = QHBoxLayout(self)
        self._layout_default = QHBoxLayout(self)
        self._layout_left = QHBoxLayout(self)
        self._layout_right = QHBoxLayout(self)

        self.__init_widget()

        # connect signal to slot
        self.parent().sizeChanged.connect(self.resize)
        self.button_minimize.clicked.connect(self.parent().showMinimized)
        self.button_zoom.clicked.connect(self.__toggleMaxState)
        self.button_close.clicked.connect(self.parent().close)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != Qt.LeftButton or not self._isDoubleClickEnabled:
            return

        self.__toggleMaxState()

    def left_add_obj(self, obj: Union[QWidget, QSpacerItem, QLayout]):
        layout_add_obj(self._layout_left, obj)

    def right_add_obj(self, obj: Union[QWidget, QSpacerItem, QLayout]):
        layout_add_obj(self._layout_right, obj)

    def resize(self, new_size: PySide6.QtCore.QSize) -> None:
        super().resize(new_size.width(), 50)

    def __init_widget(self):
        lis = [self._layout_left,
               QSpacerItem(40, 20, QSizePolicy.Expanding),
               self._layout_right,
               self._layout_default, ]
        layout_add_bojs(self._layout_main, lis)

        self.button_minimize = ToolButton(FluentIcon.MINIMIZE, self)
        self.button_zoom = ToolButton(FluentIcon.ZOOM, self)
        self.button_close = ToolButton(FluentIcon.CLOSE, self)

        # add to layout
        self._layout_default.addWidget(self.button_minimize)
        self._layout_default.addWidget(self.button_zoom)
        self._layout_default.addWidget(self.button_close)

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()


class RoundMainWindow(DefaultWidget):
    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.installEventFilter(self)

        self.title_bar = TitleBar(self)
        self.setMinimumHeight(self.title_bar.height())
        self.menu: Optional[NavigationPanel, NavigationBar] = None
        self.menu_background: Optional[DefaultWidget] = None
        self._mask = Mask(self)

        self._isResizeEnabled = True

        self.resize(500, 500)

        self.layout_main = QVBoxLayout(self)
        self.layout_main.addWidget(self.title_bar)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.setAlignment(Qt.AlignmentFlag.AlignTop)

    def install_menu(self, cls: int):
        dic = {1: NavigationPanel, 2: NavigationBar}
        self.menu_background = DefaultWidget(self)
        self.menu_background.set_widget_brush(QColor(250, 250, 250))
        self.menu_background.setMinimumSize(QSize(70, 0))
        self.menu_background.resize(70, self.height())
        self.title_bar.raise_()

        self.menu = dic[cls](self.menu_background)
        self.menu.setMinimumSize(QSize(70, 0))
        self.menu.move(0, self.title_bar.height())
        self.menu.resize(70, self.height())

        # init menu item
        self.menu.addItem("Home", FluentIcon.HOME, "HOME")
        self.menu.addItem("Search", FluentIcon.SEARCH, "SEARCH")

        new_widget = NavigationWidget(True, self)
        self.menu.addWidget("Home", new_widget)

    def eventFilter(self, obj, event):
        et = event.type()
        if et != QEvent.MouseButtonPress and et != QEvent.MouseMove or not self._isResizeEnabled:
            return False

        edges = Qt.Edge(0)
        pos = event.globalPosition() - self.pos()
        if pos.x() < self.BORDER_WIDTH:
            edges |= Qt.LeftEdge
        if pos.x() >= self.width() - self.BORDER_WIDTH:
            edges |= Qt.RightEdge
        if pos.y() < self.BORDER_WIDTH:
            edges |= Qt.TopEdge
        if pos.y() >= self.height() - self.BORDER_WIDTH:
            edges |= Qt.BottomEdge

        # change cursor
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

        elif (obj is self or obj is self.title_bar) and et == QEvent.MouseButtonPress and edges:
            self.windowHandle().startSystemResize(edges)

        return False

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if self.childAt(event.position().toPoint()) is self.title_bar:
            self.windowHandle().startSystemMove()
            event.accept()
            return

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        if self.menu_background:
            self.menu_background.resize(70, self.height())


if __name__ == "__main__":
    app = QApplication()

    w = RoundMainWindow()

    # menu1 = NavigationBar(w)
    # menu1.move(0, 50)
    # menu1.addItem("Home", FluentIcon.HOME, "HOME")
    # menu1.addItem("About", FluentIcon.INFO, "INFO")
    # menu1.resize(70, w.height())

    w.show()
    w.resize(500, 500)

    app.exec()
