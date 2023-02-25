from DataStructView.UI.BinarySearchTree import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow


class SearchTree(QMainWindow):

    def __init__(self):
        super(SearchTree, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 信号连接槽函数
        self.ui.button_add.clicked.connect(self.add)
        self.ui.button_delete.clicked.connect(self.delete)
        self.ui.button_search.clicked.connect(self.search)

    def add(self):
        print("槽函数add启动\n")

        v = self.ui.lineEdit_add.text()  # 获取输入
        self.ui.lineEdit_add.clear()  # 清除输入栏
        self.ui.graphicsView.add(v)

        print("槽函数add结束\n")

    def delete(self):
        print("槽函数delete启动\n")

        v = self.ui.lineEdit_delete.text()  # 获取输入
        self.ui.lineEdit_delete.clear()  # 清除输入栏
        self.ui.graphicsView.delete(v)

        print("槽函数delete结束\n")

    def search(self):
        print("槽函数search启动\n")

        v = self.ui.lineEdit_search.text()  # 获取输入
        self.ui.lineEdit_search.clear()  # 清除输入栏
        self.ui.graphicsView.search(v)

        print("槽函数search结束\n")


if __name__ == '__main__':
    app = QApplication()
    t = SearchTree()
    t.show()
    app.exec()
