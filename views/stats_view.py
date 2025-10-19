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

        self.current_mode = 7

        def change_mode(days):
            self.current_mode = days
            self.plot_time_per_day(days)

        self.work_timer_view_btn = QPushButton("Timer", self)

        self.week_button = QPushButton("7", self)
        self.week_button.clicked.connect(lambda: change_mode(7))

        self.month_button = QPushButton("30", self)
        self.month_button.clicked.connect(lambda: change_mode(30))

        self.half_year_button = QPushButton("6 months", self)
        self.half_year_button.clicked.connect(lambda: change_mode(182))

        self.year_button = QPushButton("1 year", self)
        self.year_button.clicked.connect(lambda: change_mode(365))

        time_buttons = QHBoxLayout()
        time_buttons.addWidget(self.week_button)
        time_buttons.addWidget(self.month_button)
        time_buttons.addWidget(self.half_year_button)
        time_buttons.addWidget(self.year_button)

        vbox = QVBoxLayout()

        vbox.addLayout(time_buttons)

        self.df = self.build_full_df()

        # Create matplotlib Figure and Canvas
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        vbox.addWidget(self.canvas)

        #self.draw_plot()

        vbox.addWidget(self.work_timer_view_btn)
        self.setLayout(vbox)

        self.work_timer_view_btn.clicked.connect(self.switch_to_timer)


    def build_full_df(self):
        end_date = pd.to_datetime(QDate.currentDate().toString("yyyy-MM-dd"))
        start_date = end_date - pd.Timedelta(days=5*365)

        full_dates = pd.date_range(start=start_date, end=end_date)
        df = pd.DataFrame({'date': full_dates, 'seconds': 0.0})

        
        db_data = db.get_all_data()  
        db_df = pd.DataFrame(db_data, columns=['date', 'time'])
        db_df['date'] = pd.to_datetime(db_df['date'])

        def time_to_seconds(t):
            h, m, s = t.split(':')
            return int(h)*3600 + int(m)*60 + float(s)
        
        db_df['seconds'] = db_df['time'].apply(time_to_seconds)
        db_df = db_df[['date', 'seconds']]

        # Merge and fill missing with 0
        merged = pd.merge(df, db_df, on='date', how='left')
        merged['seconds'] = merged['seconds_y'].fillna(merged['seconds_x'])
        merged = merged[['date', 'seconds']]

        return merged


    def draw_plot(self, new_seconds):
            today = pd.to_datetime(QDate.currentDate().toString("yyyy-MM-dd"))
            self.df.loc[self.df['date'] == today, 'seconds'] = new_seconds
            self.plot_time_per_day(self.current_mode)

    def get_window_df(self, days):
            end_date = self.df['date'].max()
            start_date = end_date - pd.Timedelta(days=days)
            return self.df[(self.df['date'] >= start_date) & (self.df['date'] <= end_date)]

    def plot_time_per_day(self, days):

        current_df = self.get_window_df(days).copy()

        current_df = current_df.sort_values('date')

        weekday_labels = current_df['date'].dt.strftime('%a').str.upper()

        self.ax.clear()
        self.ax.plot(current_df['date'], current_df['seconds'], marker='o', linestyle='-')

        self.ax.set_xticks(current_df['date'])
        if self.current_mode == 7:
            self.ax.set_xticklabels(weekday_labels)
        else:
            self.ax.set_xticklabels([])

        min_date = current_df['date'].min()
        max_date = current_df['date'].max()
        self.ax.set_xlim(min_date, max_date + pd.Timedelta(days=0.5))


        self.ax.grid(True)
        #self.figure.autofmt_xdate()  # Rotate date labels for readability
        self.ax.set_ylim(bottom=0)
        ymax = self.df['seconds'].max() * 1.2  # 20% margin above highest point
        self.ax.set_ylim(0, ymax)
        self.canvas.draw()


        
        
