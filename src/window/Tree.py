import PySide6
from ui.BinaryTree_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow


class Tree(QMainWindow):
    def __init__(self):
        super(Tree, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication()
    t = Tree()
    t.show()
    app.exec()
