import PySide6

from enum import Enum
from PySide6.QtCore import Qt, Signal
from qfluentwidgets import FlyoutView, PushButton, Flyout, FluentIcon
from src.tool import PathTool


class DataStructureImagePath:
    path = PathTool.root_path + "/images/datastructure/"
    HEAP = ""
    HASH = ""
    STACK = ""
    GRAPH = path + "graph.png"
    BINARY_TREE = path + "binary_tree.png"
    SEGMENT_TREE = path + "segment_tree.png"


class FlyoutViewButton(PushButton):
    enterIntoSignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.clicked.connect(self.show_flyout_view)

    def show_flyout_view(self):
        raise NotImplementedError


class Heap(FlyoutViewButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Heap")

    def show_flyout_view(self):
        content = "Data-SGV:   This is Heap view."

        view = FlyoutView(
            title="Heap",
            content=content,
            image=DataStructureImagePath.HEAP,
            isClosable=True
        )

        init_view(self, view)


class Hash(FlyoutViewButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Hash")

    def show_flyout_view(self):
        content = "Data-SGV:   This is Hash view."

        view = FlyoutView(
            title="Hash",
            content=content,
            image=DataStructureImagePath.HASH,
            isClosable=True
        )

        init_view(self, view)


class Graph(FlyoutViewButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Graph")

    def show_flyout_view(self):
        content = \
            """
            Data-SGV:   This is Graph view.
            """

        view = FlyoutView(
            title="Graph",
            content=content,
            image=DataStructureImagePath.GRAPH,
            isClosable=True
        )

        init_view(self, view)


class Stack(FlyoutViewButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Stack")

    def show_flyout_view(self):
        content = "Data-SGV:   This is Stack view."

        view = FlyoutView(
            title="Stack",
            content=content,
            image=DataStructureImagePath.STACK,
            isClosable=True
        )

        init_view(self, view)


class BinaryTree(FlyoutViewButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("BinaryTree")

    def show_flyout_view(self):
        content = \
            """
            Data-SGV:   This is BinaryTree view.
            """

        view = FlyoutView(
            title="BinaryTree",
            content=content,
            image=DataStructureImagePath.BINARY_TREE,
            isClosable=True
        )

        init_view(self, view)


class SegmentTree(FlyoutViewButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("SegmentTree")

    def show_flyout_view(self):
        content = "Data-SGV:   This is SegmentTree view."

        view = FlyoutView(
            title="SegmentTree",
            content=content,
            image=DataStructureImagePath.SEGMENT_TREE,
            isClosable=True
        )

        init_view(self, view)


class FlyoutViewButtonEnum(Enum):
    HEAP = "Heap"
    HASH = "Hash"
    GRAPH = "Graph"
    STACK = "Stack"
    BINARY_TREE = "BinaryTree"
    SEGMENT_TREE = "SegmentTree"


class ViewButton:
    enum_to_object = {
        FlyoutViewButtonEnum.HEAP: Heap,
        FlyoutViewButtonEnum.HASH: Hash,
        FlyoutViewButtonEnum.GRAPH: Graph,
        FlyoutViewButtonEnum.STACK: Stack,
        FlyoutViewButtonEnum.BINARY_TREE: BinaryTree,
        FlyoutViewButtonEnum.SEGMENT_TREE: SegmentTree,
    }

    @classmethod
    def create_button(cls, enum: FlyoutViewButtonEnum, parent=None):
        if enum not in cls.enum_to_object:
            raise ValueError(f"enum {enum} is not supported")
        button = cls.enum_to_object[enum](parent)
        return button


def init_view(f_v_button: FlyoutViewButton, view: FlyoutView):
    # add button to view
    button = PushButton("ENTER INTO", parent=view)
    button.setFixedWidth(120)
    button.clicked.connect(f_v_button.enterIntoSignal)
    view.addWidget(button, align=Qt.AlignRight)

    # adjust layout
    view.widgetLayout.insertSpacing(1, 5)
    view.widgetLayout.addSpacing(5)

    w = Flyout.make(view, f_v_button, f_v_button.parent())
    view.closed.connect(w.close)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QWidget

    app = QApplication()
    w = QWidget()
    w.resize(500, 500)
    b = ViewButton.create_button(FlyoutViewButtonEnum.BINARY_TREE, w)
    b.move(100, 100)
    b2 = ViewButton.create_button(FlyoutViewButtonEnum.GRAPH, w)
    b2.move(100, 200)
    w.show()
    app.exec()
