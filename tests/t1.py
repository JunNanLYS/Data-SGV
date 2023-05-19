from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication, QGraphicsItem

from src.widgets import line_item
from src.widgets.line_item import Line
from src.data_structure.graph import GraphNode
from src.widgets.graphics_view import GraphView

# node1, node2 = GraphNode('1'), GraphNode('2')


app = QApplication()
view = GraphView()

ZheJiang = GraphNode('Name1')
ShangHai = GraphNode('Name2')
view.scene.addItem(ZheJiang)
view.scene.addItem(ShangHai)
view.nodes['Name1'] = ZheJiang
view.nodes['Name2'] = ShangHai
ZheJiang.setPos(QPointF(300, 100))
ShangHai.setPos(QPointF(400, 100))
print(isinstance(ZheJiang, QGraphicsItem))

line2 = line_item.LineToEllipse(ZheJiang, ShangHai)
line3 = line_item.LineWithWeight(ZheJiang, ShangHai)
line4 = line_item.ArrowLine(ZheJiang, ShangHai)
line5 = line_item.ArrowLineWithWeight(ZheJiang, ShangHai)

print(isinstance(line2, QGraphicsItem))
print(isinstance(line3, QGraphicsItem))
print(isinstance(line4, QGraphicsItem))
print(isinstance(line5, QGraphicsItem))

view.show()
app.exec()


