from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QSizePolicy, QLabel, QGridLayout
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem
from qfluentwidgets import ToolButton, FluentIcon, Dialog

from src.widgets.button import PixmapButton
from src.widgets.data_structure_windows import TreeDataStructure, GraphDataStructure
from src.widgets.windows import RoundedWindow


class MainWindow(RoundedWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tree = TreeDataStructure()
        self.graph = GraphDataStructure()

        self.__init_widget()

        # signal connect slot
        self.button_close.clicked.connect(self.close)
        self.button_tree.clicked.connect(self.tree.show)
        self.button_graph.clicked.connect(self.graph.show)
        self.button_heap.clicked.connect(function_dialog)

    def __init_widget(self):
        # init font
        font_title = QFont()
        font_title.setPointSize(20)
        font_title.setFamily("Segoe")
        font_title.setBold(True)

        self.layout_main = QVBoxLayout(self)

        # tools layout
        layout_tools = QHBoxLayout()
        self.button_info = ToolButton(FluentIcon.INFO, self)
        self.button_zoom = ToolButton(FluentIcon.ZOOM, self)
        self.button_close = ToolButton(FluentIcon.CLOSE, self)

        # data structure
        label_title = QLabel("Data Structure", self)
        label_title.setFont(font_title)
        label_title.setAlignment(Qt.AlignCenter)

        layout_buttons = QGridLayout()
        self.button_tree = PixmapButton("Binary Tree", self)
        pix = QPixmap("images/binary_tree.png")
        self.button_tree.set_image(pix)

        self.button_graph = PixmapButton("Graph", self)
        pix = QPixmap("images/graph.png")
        self.button_graph.set_image(pix)

        self.button_segment = PixmapButton("Segment Tree", self)
        pix = QPixmap("images/graph.png")
        self.button_segment.set_image(pix)

        self.button_heap = PixmapButton("Heap", self)

        self.button_stack = PixmapButton("Stack", self)

        self.button_hash = PixmapButton("Hash", self)

        # add to layout
        layout_tools.addWidget(self.button_info)
        layout_tools.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout_tools.addWidget(self.button_zoom)
        layout_tools.addWidget(self.button_close)

        layout_buttons.addWidget(self.button_tree, 0, 0)
        layout_buttons.addWidget(self.button_graph, 0, 1)
        layout_buttons.addWidget(self.button_segment, 0, 2)
        layout_buttons.addWidget(self.button_hash, 1, 0)
        layout_buttons.addWidget(self.button_stack, 1, 1)
        layout_buttons.addWidget(self.button_heap, 1, 2)

        self.layout_main.addLayout(layout_tools)
        self.layout_main.addWidget(label_title)
        self.layout_main.addLayout(layout_buttons)
        self.layout_main.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))


def function_dialog():
    dialog = Dialog("", "The function is temporarily unavailable")
    dialog.show()


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
