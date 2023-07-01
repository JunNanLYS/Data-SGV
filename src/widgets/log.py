from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont, QTextCharFormat
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import PlainTextEdit, Dialog


class LogWidget(PlainTextEdit):
    add = Signal(str)
    added = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)  # only read
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedSize(self.sizeHint())
        self.setMinimumSize(50, 50)

        # init font
        fmt = QTextCharFormat()
        fmt.setFontPointSize(12)
        self.mergeCurrentCharFormat(fmt)

        self.setMinimumSize(50, 50)
        self.setMaximumSize(1000, 500)

        # signal connect slot
        self.add.connect(self.receive_message)

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
    # log_widget.resize(500, 500)
    # log_widget.setMinimumSize(600, 600)
    nums = [x for x in range(9999999999, 10000000000)]
    window.show()
    for num in nums:
        log_widget.add.emit(f"log{num}")
    log_widget.add.emit("11111111111111111111111111111111111111111111")
    app.exec()
