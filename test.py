import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget
import serial

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial_port = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port and baud rate as needed

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_data)
        layout.addWidget(send_button)

    def send_data(self):
        data = self.line_edit.text().encode()
        self.serial_port.write(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
