from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import PlainTextEdit, Dialog


class LogWidget(PlainTextEdit):
    add = Signal(str)  # 接收log的信号
    added = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)  # 只读不写
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedSize(self.sizeHint())

        self.add.connect(self.receive_message)  # 信号连接发送Log的槽函数

    def append(self, text):
        """新增Log"""
        self.appendPlainText(text)
        self.added.emit()

    @Slot(str)
    def receive_message(self, message: str):
        self.append(message)


if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    window.resize(800, 600)
    dig = Dialog("Error", "Type Error", window)
    log_widget = LogWidget(window)
    nums = [x for x in range(100, 1000)]
    window.show()
    for num in nums:
        log_widget.add.emit(f"log{num}")
    app.exec()
