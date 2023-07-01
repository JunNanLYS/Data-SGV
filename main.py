from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QApplication, QSizePolicy, QLabel, QGridLayout
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem
from qfluentwidgets import ToolButton, FluentIcon, Dialog

from src.widgets.button import PixmapButton
from src.widgets.data_structure_windows import TreeDataStructure, GraphDataStructure, SegmentTreeDataStructure
from src.widgets.window import RoundMainWindow
from src.widgets.flyout_view_button import FlyoutViewButtonEnum, ViewButton


class MainWindow(RoundMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setResizeEnabled(False)

        self.tree = TreeDataStructure()
        self.graph = GraphDataStructure()
        self.segment_tree = SegmentTreeDataStructure()

        self.__init_widget()

        # signal connect slot
        self.button_tree.enterIntoSignal.connect(self.tree.show)
        self.button_graph.enterIntoSignal.connect(self.graph.show)
        self.button_segment.enterIntoSignal.connect(self.segment_tree.show)

    def __init_widget(self):
        # init font
        font_title = QFont()
        font_title.setPointSize(20)
        font_title.setFamily("Segoe")
        font_title.setBold(True)

        # data structure
        label_title = QLabel("Data Structure", self)
        label_title.setFont(font_title)
        label_title.setAlignment(Qt.AlignCenter)

        layout_buttons = QGridLayout()
        layout_buttons.setSpacing(5)
        self.button_tree = ViewButton.create_button(FlyoutViewButtonEnum.BINARY_TREE, self)

        self.button_graph = ViewButton.create_button(FlyoutViewButtonEnum.GRAPH, self)

        self.button_segment = ViewButton.create_button(FlyoutViewButtonEnum.SEGMENT_TREE, self)

        self.button_heap = ViewButton.create_button(FlyoutViewButtonEnum.HEAP, self)

        self.button_stack = ViewButton.create_button(FlyoutViewButtonEnum.STACK, self)

        self.button_hash = ViewButton.create_button(FlyoutViewButtonEnum.HASH, self)

        layout_buttons.addWidget(self.button_tree, 0, 0)
        layout_buttons.addWidget(self.button_graph, 0, 1)
        layout_buttons.addWidget(self.button_segment, 0, 2)
        layout_buttons.addWidget(self.button_hash, 1, 0)
        layout_buttons.addWidget(self.button_stack, 1, 1)
        layout_buttons.addWidget(self.button_heap, 1, 2)

        self.layout_main.setSpacing(10)
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
