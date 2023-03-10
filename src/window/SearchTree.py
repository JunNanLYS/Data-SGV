import asyncio
import PySide6
from PySide6.QtCore import Qt, QPointF, QPoint, QFile, Property, QPropertyAnimation, QThread, QTime, QCoreApplication, \
    QEventLoop
from PySide6.QtGui import QGuiApplication, QScreen

from ui.BinarySearchTree_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow
from src.window.Setting import SettingWidget


def split(s: str) -> list[str]:
    """
    用于处理用户输入的非法字符

    一共会出现以下几种情况
    1. 有非法字符
        非法字符混杂在逗号中
        非法字符混杂在数字中
            跳过非法字符直到 s[i] == digit 或者 s[i] == ',' or '，' 或者 i == n
    2. 无非法字符
        正常查找
    """
    res = []
    i, n = 0, len(s)
    while i < n:
        while i < n and (s[i] == ',' or s[i] == '，' or (s[i] != ',' and s[i] != '，' and not (s[i].isdigit()))):
            i += 1
        i = i
        c = ""
        while i < n and (s[i].isdigit() or (s[i] != ',' and s[i] != '，')):
            if s[i].isdigit():
                c += s[i]
            i += 1
        if c: res.append(c)
        i = i
    return res


def stopTime(x: int, state=False):
    endTime = QTime.currentTime().addMSecs(x) if state else QTime.currentTime().addSecs(x)
    while QTime.currentTime() < endTime:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)


class SearchTree(QMainWindow):

    def __init__(self):
        super(SearchTree, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)  # MainWindow自带的栏隐藏
        self.setAttribute(Qt.WA_TranslucentBackground)  # MainWindow背景隐藏

        # MyWidget 设置
        self.setting_widget = SettingWidget(self.ui.widget)  # 用于设置的窗口
        self.setting_widget.hide()

        self.widget_enlarge_cnt = 0  # 0未放大 1已放大
        self.ui.widget.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)  # widget主窗口 | 标题栏隐藏
        self.ui.widget.setAttribute(Qt.WA_TranslucentBackground)  # 背景无绘制
        self.ui.widget.showNormal()
        self.move_to_desktop_center(self.ui.widget)

        # 信号连接槽函数
        self.ui.button_add.clicked.connect(self.add)
        self.ui.button_delete.clicked.connect(self.delete)
        self.ui.button_search.clicked.connect(self.search)

        self.ui.button_preorder.clicked.connect(self.traversal_pre)
        self.ui.button_inorder.clicked.connect(self.traversal_in)
        self.ui.button_postorder.clicked.connect(self.traversal_post)

        self.ui.button_enlarge.clicked.connect(self.enlarge)
        self.ui.button_setting.clicked.connect(self.open_setting)

        self.setting_widget.ui.button_close.clicked.connect(self.close_setting)

    def add(self):
        """
        测试数据: 10,5,3,1,2,4,7,6,8,9,15,13,12,11,14,17,16
        """
        print("槽函数add启动\n")
        self.ui.graphicsView.redraw()

        v = self.ui.lineEdit_add.text()  # 获取输入
        self.ui.lineEdit_add.clear()  # 清除输入栏
        self.ui.graphicsView.add(v)

        print("槽函数add结束\n")

    def delete(self):
        print("槽函数delete启动\n")
        self.ui.graphicsView.redraw()

        v = self.ui.lineEdit_delete.text()  # 获取输入
        if not v or len(split(v)) > 1: return
        self.ui.lineEdit_delete.clear()  # 清除输入栏
        self.ui.graphicsView.delete(v)

        print("槽函数delete结束\n")

    # 放大槽函数
    def enlarge(self):
        widget = self.ui.widget
        self.widget_enlarge_cnt ^= 1
        if self.widget_enlarge_cnt:
            widget.pre_pos = self.ui.widget.pos()
            widget.setWindowFlags(Qt.Window)
            widget.showFullScreen()
        else:
            widget.setWindowFlags(Qt.SubWindow)
            widget.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
            widget.setAttribute(Qt.WA_TranslucentBackground)
            widget.showNormal()
            widget.resize(widget.minimumSize())
            # 由于缩小以后widget会移动到左上角，我们需要手动将其移动到屏幕中心
            self.move_to_desktop_center(widget)

    def move_to_desktop_center(self, widget):
        """将widget移动到屏幕中间"""
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()  # 获取当前主屏幕的像素区域
        width, height = widget.width(), widget.height()  # 获取widget的宽度与高度
        width /= 2
        height /= 2
        widget.move(center.x() - width, center.y() - height)  # 移动

    def search(self):
        print("槽函数search启动\n")
        self.ui.graphicsView.redraw()

        v = self.ui.lineEdit_search.text()  # 获取输入
        if not v and len(split(v)) > 1: return
        self.ui.lineEdit_search.clear()  # 清除输入栏
        self.ui.graphicsView.search(v)

        print("槽函数search结束\n")

    def traversal_pre(self):
        self.ui.graphicsView.redraw()
        self.ui.graphicsView.traversal_pre_animation()

    def traversal_in(self):
        self.ui.graphicsView.redraw()
        self.ui.graphicsView.traversal_in_animation()

    def traversal_post(self):
        self.ui.graphicsView.redraw()
        self.ui.graphicsView.traversal_post_animation()

    @Property(QPoint)
    def setting_move_animation(self):
        # print("Property get")
        return QPoint(0, 0)

    @setting_move_animation.setter
    def setting_move_animation(self, p):
        # print("Property set")
        self.setting_widget.move(p)

    def start_animation(self, **kwargs):
        state = kwargs.get("state", "open")  # 默认打开模式 | 若传入state为close则为关闭模式
        animations = QPropertyAnimation(self)
        animations.setTargetObject(self)
        animations.setPropertyName(b'setting_move_animation')
        width = self.setting_widget.width()  # setting宽度
        if state == "open":
            animations.setStartValue(QPoint(-width, 0))
            animations.setEndValue(QPoint(0, 0))
        else:
            animations.setStartValue(QPoint(0, 0))
            animations.setEndValue(QPoint(-width, 0))
        animations.setDuration(500)  # 若要修改该时间则要把下面的协程等待时间一起修改了
        animations.start()

    def open_setting(self):
        self.setting_widget.show()
        self.start_animation()
        print("open setting")

    def close_setting(self):
        self.start_animation(state="close")
        stopTime(500, state=True)
        self.setting_widget.hide()
        print("close setting")


if __name__ == '__main__':
    app = QApplication()
    t = SearchTree()
    t.show()
    app.exec()
