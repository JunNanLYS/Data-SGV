from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QPlainTextEdit, QApplication, QWidget, QPushButton, QMainWindow
from qfluentwidgets import PlainTextEdit


class LogWidget(PlainTextEdit):
    log_signal = Signal(str)  # 接收log的信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)  # 只读不写
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedSize(self.sizeHint())

        self.log_signal.connect(self.receive_message)  # 信号连接发送Log的槽函数

    def append(self, text):
        """新增Log"""
        self.appendPlainText(text)

    @Slot(str)
    def receive_message(self, message: str):
        self.append(message)


if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    window.resize(800, 600)
    log_widget = LogWidget(window)
    nums = [x for x in range(100, 1000)]
    for num in nums:
        log_widget.log_signal.emit(f"log{num}")
    window.show()
    app.exec()
