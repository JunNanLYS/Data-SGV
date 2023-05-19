from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QPlainTextEdit, QApplication, QWidget, QPushButton, QMainWindow


class LogWidget(QPlainTextEdit):
    log_signal = Signal(str)  # 接收log的信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)  # 只读不写
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedSize(self.sizeHint())
        self.set_style_sheet()

        self.log_signal.connect(self.receive_message)  # 信号连接发送Log的槽函数

    def append(self, text):
        """新增Log"""
        self.appendPlainText(text)

    @Slot(str)
    def receive_message(self, message: str):
        self.append(message)

    def set_style_sheet(self):
        self.setStyleSheet("""
        QPlainTextEdit{
        background-color: rgb(245, 245, 245);
        border-radius: 12px;
        }
        """)


if __name__ == "__main__":
    app = QApplication([])
    app.exec()
