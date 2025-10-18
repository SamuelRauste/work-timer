from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget
from PyQt5.QtCore import Qt, QTimer, QTime, QDate, pyqtSignal
import db
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# The view where statistics will be displayed

class StatsWindow(QWidget):
    switch_to_timer = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.work_timer_view_btn = QPushButton("Timer", self)

        vbox = QVBoxLayout()

        self.data = db.get_all_data()

        self.df = pd.DataFrame(self.data, columns=['date', 'time'])
        self.df['date'] = pd.to_datetime(self.df['date'])

        def time_to_seconds(t):
            h, m, s = t.split(':')
            return int(h)*3600 + int(m)*60 + float(s)

        self.df['seconds'] = self.df['time'].apply(time_to_seconds)
        self.df = self.df.sort_values('date')


        # Create matplotlib Figure and Canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        vbox.addWidget(self.canvas)

        # Plot the data
        self.plot_time_per_day()

        
        vbox.addWidget(self.work_timer_view_btn)
        self.setLayout(vbox)

        self.work_timer_view_btn.clicked.connect(self.switch_to_timer)


    def plot_time_per_day(self):
        self.ax.clear()
        self.ax.plot(self.df['date'], self.df['seconds'], marker='o', linestyle='-')
        self.ax.set_title("Time per Day")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Time (seconds)")
        self.ax.grid(True)
        self.figure.autofmt_xdate()  # Rotate date labels for readability
        self.canvas.draw()


        
        
