import sys

import serial
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QDialog, QVBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import random

class Control(QMainWindow):
    def __init__(self):
        super(Control,self).__init__()
        loadUi("untitled.ui",self)
        #self.serial_port = serial.Serial('/dev/ttyUSB0', 9600)
        self.setWindowTitle("Electrical Stimulation Control")
        self.submitbutton.clicked.connect(self.submitfunction)
        self.set_text()
        self.type_ipt.activated[str].connect(self.type_selection)

        # Create a Matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.addWidget(self.canvas)

        # Add a subplot to the figure
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.set_title('Real-Time Graph')

        # Initialize an empty line
        self.line, = self.ax.plot([], [], 'b-')

        # Data containers
        self.x_data = []
        self.y_data = []

        # Create a QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

    def update_plot(self):
        # Generate random data for demonstration
        x = len(self.x_data)
        y = random.random()

        # Append new data
        self.x_data.append(x)
        self.y_data.append(y)

        # Limit data to display (optional)
        # if len(self.x_data) > 50:
        #     self.x_data.pop(0)
        #     self.y_data.pop(0)

        # Update plot
        self.line.set_data(self.x_data, self.y_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def is_integer(self, *texts):
        for text in texts:
            if not text.isdigit():
                return False
        return True

    def submitfunction(self):
        pulse_duration_text = self.pulse_duration_ipt.text()
        count_of_pulses_text = self.count_of_pulses_ipt.text()
        no_of_signal_text = self.no_of_signals_ipt.text()
        delay_btw_pulses_text = self.delay_btw_pulses_ipt.text()
        if self.is_integer(pulse_duration_text,count_of_pulses_text,no_of_signal_text,delay_btw_pulses_text):
            print(self.pulse_duration_ipt.text())
            print(self.count_of_pulses_ipt.text())
            print(self.no_of_signals_ipt.text())
            print(self.delay_btw_pulses_ipt.text())
        else:
            print("Input should be Integer values.")

    def set_text(self):
        text = "Computed output values"
        self.output_data.setText(text)

    def send_data(self):
        data = self.pulse_duration_ipt.text().encode()
        self.serial_port.write(data)

    def type_selection(self, text):
        print("Selected value:", text)


app=QApplication(sys.argv)
mainwindow = Control()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.resize(900, 800)
widget.show()
app.exec_()