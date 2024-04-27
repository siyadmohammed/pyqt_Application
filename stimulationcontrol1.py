import os
import sys

import serial
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ser = serial.Serial('COM3', 115200)

class Control(QMainWindow):
    def __init__(self):
        super(Control, self).__init__()
        self.ser = None
        script_dir = os.path.dirname(sys.argv[0])
        ui_file = os.path.join(script_dir, "untitled.ui")
        loadUi(ui_file, self)
        self.setWindowTitle("Electrical Stimulation Control")
        self.submitbutton.clicked.connect(self.send_data)
        self.type_ipt.activated[str].connect(self.type_selection)
        self.data = []  # List to store the incoming data
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(50)  # Update plot every 50 milliseconds
        self.initUI()

    def is_integer(self, *texts):
        for text in texts:
            if not text.isdigit():
                return False
        return True

    def type_selection(self, text):
        self.selected_type = text

    def send_data(self):
        port = self.port_inpt.text()
        self.ser = serial.Serial(port, 115200)
        frequency = self.frequency.text()
        total_session_time = self.total_session_time.text()
        max_current = self.max_current.text()
        if self.is_integer(frequency, total_session_time, max_current):
            data1 = self.frequency.text().encode()
            data2 = self.total_session_time_text.encode()
            data3 = self.max_current_text.encode()
            self.ser.write(data1 + b" " + data2 + b" " + data3 + b" " + self.selected_type.encode())
        else:
            print("Input should be Integer values.")

    def initUI(self):

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        canvas_layout = QtWidgets.QVBoxLayout(self.frame)
        canvas_layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)

    def update_plot(self):
        if self.ser and self.ser.inWaiting():
            data_point = self.ser.readline().decode().strip()
            if data_point:
                if data_point.isdigit():
                    self.data.append(int(data_point))
            else:
                print("no output")

        self.ax.clear()
        self.ax.plot(self.data)
        self.canvas.draw()


app = QApplication(sys.argv)
mainwindow = Control()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.resize(1200, 1200)
widget.show()
app.exec_()
