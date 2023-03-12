import os.path

import PySide6
from PySide6.QtCore import Qt, QPoint, QRect, Property, QPropertyAnimation, QPointF
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QScrollArea, QVBoxLayout, QSlider, QPushButton, \
    QGraphicsBlurEffect, QGraphicsOpacityEffect, QGroupBox


class BlackMask(QWidget):
    """黑色透明遮罩"""

    def __init__(self, parent=None):
        super(BlackMask, self).__init__(parent)
        self.effect = QGraphicsOpacityEffect()
        self.effect.setOpacity(0.5)  # 半透明
        self.setGraphicsEffect(self.effect)

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        """不接收鼠标点击"""
        pass

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(Qt.gray))
        painter.drawRoundedRect(self.rect(), 20, 20)


class MyWidget(QWidget):
    mouse = Qt.MouseButton.NoButton  # 记录鼠标
    lastPos = PySide6.QtCore.QPointF()  # 记录鼠标点击的位置
    brush = QBrush(QColor(245, 245, 245))

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.mouse = PySide6.QtCore.Qt.MouseButton.NoButton
        self.item = False  # 当点击空白处时为False
        self.border = False  # 鼠标是否在边框的边上
        # 设置 Setting
        self.setWindowFlags(Qt.FramelessWindowHint)  # 菜单栏
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景绘制
        self.setAttribute(Qt.WA_StyledBackground, True)  # 继承绘制
        self.setMouseTracking(True)  # 鼠标拖动

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        # print("MyWidget: 鼠标点击")
        self.mouse = event.button()
        self.item = self.childAt(event.pos()) is None
        if event.button() == Qt.MouseButton.LeftButton and self.item:
            self.lastPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if self.mouse == Qt.MouseButton.LeftButton:
            self.move(self.mapToGlobal(event.pos() - self.lastPos))

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = Qt.MouseButton.NoButton
        QWidget.mouseReleaseEvent(self, event)

    def set_brush_color(self, brush: QBrush):
        """用于修改控件颜色"""
        self.brush = brush
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(self.rect(), 20, 20)


class MyMainWindow(QMainWindow):
    mouse = Qt.MouseButton.NoButton  # 记录鼠标
    lastPos = PySide6.QtCore.QPointF()  # 记录鼠标点击的位置

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.mouse = PySide6.QtCore.Qt.MouseButton.NoButton
        self.item = False  # 当点击空白处时为False
        self.border = False  # 鼠标是否在边框的边上
        # 设置 Setting
        self.setWindowFlags(Qt.FramelessWindowHint)  # 菜单栏
        self.setAttribute(Qt.WA_StyledBackground, True)  # 继承绘制
        self.setMouseTracking(True)  # 鼠标拖动

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = event.button()
        self.item = self.childAt(event.pos()) is None
        if event.button() == Qt.MouseButton.LeftButton and self.item:
            self.lastPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if self.mouse == Qt.MouseButton.LeftButton and self.item:
            self.move(self.mapToGlobal(event.pos() - self.lastPos))

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        self.mouse = Qt.MouseButton.NoButton
        QWidget.mouseReleaseEvent(self, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(245, 245, 245)))
        painter.drawRoundedRect(self.rect(), 20, 20)


class MyGroupBox(QGroupBox):
    brush = QBrush(QColor(0, 0, 0))

    def __init__(self, title: str, parent=None):
        super(MyGroupBox, self).__init__(title, parent)

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        """不接收鼠标事件"""
        pass

    def set_brush_color(self, brush: QBrush):
        self.brush = brush
        self.update()

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        super().paintEvent(event)


class MyScrollArea(QScrollArea):
    """滚动视图"""

    def __init__(self, width=100, high=100, parent=None):
        super(MyScrollArea, self).__init__(parent)
        self.mouse = Qt.MouseButton.NoButton
        # self.resize(width, high)  # 设置大小
        self.scroll_widget = ScrollAreaWidget()
        self.layout = QVBoxLayout(self.scroll_widget)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 垂直滑动条隐藏
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 水平滑动条隐藏

    # 设置样式表
    def set_style_sheet(self):
        with open("../../qss/ScrollArea.qss", "r") as f:
            scroll_area_qss = f.read()
        self.setStyleSheet(scroll_area_qss)


class MyButton(QPushButton):
    def __init__(self, parent=None):
        super(MyButton, self).__init__(parent)
        self.set_qss()

    def set_qss(self):
        path = os.path.dirname(__file__)
        for _ in range(2):
            path = os.path.dirname(path)
        # 样式表路径
        path += "\qss\MyButton.qss"
        with open(path, "r") as f:
            qss = f.read()
        self.setStyleSheet(qss)


class IconButton(QPushButton):
    """Icon按钮"""

    def __init__(self, parent=None):
        super(IconButton, self).__init__(parent)
        self.set_style()  # 控件样式

    def set_style(self):
        """用于加载qss"""
        with open("../../qss/IconButton.qss", "r") as f:
            qss = f.read()
        self.setStyleSheet(qss)


class StyleButton(QPushButton):
    """样式按钮"""
    brush = Qt.gray

    def __init__(self, parent=None):
        self.animation_speed = 0.5  # second
        super(StyleButton, self).__init__(parent)
        self._rect_ellipse_height = 20
        self._rect_rectangle_height = 0  # 矩形默认0，当button被选中时调用动画
        self.toggled.connect(self.line_animation)  # checked信号
        self.set_style()

    def set_style(self):
        """用于加载qss"""
        with open("../../qss/StyleButton.qss", "r") as f:
            qss = f.read()
        self.setStyleSheet(qss)

    def set_brush_color(self, brush: QBrush):
        self.brush = brush
        self.update()  # 重绘

    @Property(int)
    def button_update(self):
        return self._rect_rectangle_height

    @button_update.setter
    def button_update(self, height):
        self._rect_rectangle_height = height
        self.update()

    def line_animation(self):
        animation = QPropertyAnimation(self)
        animation.setTargetObject(self)
        animation.setPropertyName(b"button_update")
        if self.isChecked():
            animation.setStartValue(self._rect_rectangle_height)
            animation.setEndValue(self.rect().height() - self._rect_ellipse_height * 2)  # 极限为button高 - 圆直径 * 2
        else:
            animation.setStartValue(self._rect_rectangle_height)
            animation.setEndValue(0)
        animation_speed = self.animation_speed * 1000  # 1s = 1000ms
        animation.setDuration(animation_speed)
        animation.start()

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        """
        绘制一个矩形 + 两个椭圆
        """
        super().paintEvent(event)  # 继承原来的绘制
        rect_button = self.rect()  # 原Button的rect
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush)
        rect_ellipse_top = QRect(
            0, 0, self._rect_ellipse_height, self._rect_ellipse_height
        )  # 矩形上面的圆
        rect_ellipse_down = QRect(
            0, 0, self._rect_ellipse_height, self._rect_ellipse_height
        )  # 矩形下面的圆
        rect_rectangle = QRect(
            0, 0, self._rect_ellipse_height, self._rect_rectangle_height
        )  # 矩形

        # 先绘制矩形再绘制上下两个圆
        rect_rectangle.moveCenter(QPoint(15, rect_button.height() // 2))  # 矩形中心移动到(15, button高度中心)
        rectangle_height = rect_rectangle.height() // 2
        pos_top = QPoint(15, rect_button.height() // 2 - rectangle_height)  # 圆心1
        pos_down = QPoint(15, rect_button.height() // 2 + rectangle_height)  # 圆心2
        rect_ellipse_top.moveCenter(pos_top)  # 移动圆心
        rect_ellipse_down.moveCenter(pos_down)  # 移动圆心

        # 绘制
        painter.drawRect(rect_rectangle)
        painter.drawEllipse(rect_ellipse_top)
        painter.drawEllipse(rect_ellipse_down)


class ScrollAreaBackGround(MyWidget):
    """
    与ScrollArea进行配合，主要功能就是接收子widget鼠标事件并做出反应
    """

    def __init__(self, parent=None):
        super(ScrollAreaBackGround, self).__init__(parent)

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        pass

    def mouseMoveEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        pass


class ScrollAreaWidget(QWidget):
    """滚动视图下的widget"""

    def __init__(self, parent=None):
        super(ScrollAreaWidget, self).__init__(parent)
        self.mouse = Qt.MouseButton.NoButton

    def paintEvent(self, event: PySide6.QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(245, 245, 245)))
        painter.drawRoundedRect(self.rect(), 0, 0)


class StyleSlider(QSlider):
    def __init__(self, parent=None):
        super(StyleSlider, self).__init__(parent)
        # self.setOrientation(Qt.Horizontal)
        self.set_style()

    def set_style(self):
        with open("../../qss/StyleSlider.qss", "r") as f:
            qss = f.read()
        self.setStyleSheet(qss)


if __name__ == '__main__':
    app = QApplication()
    window = QWidget()
    button = StyleButton(window)
    button.move(250, 250)
    button.resize(100, 100)
    window.resize(500, 500)
    window.show()
    app.exec()
