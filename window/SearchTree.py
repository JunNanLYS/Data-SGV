from DataStructureGraphicsView.UI.BinarySearchTree_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow


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

class SearchTree(QMainWindow):

    def __init__(self):
        super(SearchTree, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 信号连接槽函数
        self.ui.button_add.clicked.connect(self.add)
        self.ui.button_delete.clicked.connect(self.delete)
        self.ui.button_search.clicked.connect(self.search)

        self.ui.button_preorder.clicked.connect(self.traversal_pre)
        self.ui.button_inorder.clicked.connect(self.traversal_in)
        self.ui.button_postorder.clicked.connect(self.traversal_post)

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


if __name__ == '__main__':
    app = QApplication()
    t = SearchTree()
    t.show()
    app.exec()
