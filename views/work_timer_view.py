from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QTime, QDate, QSize, pyqtSignal
from datetime import datetime
import db

# The view for the actual timer and its functionalities

def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%d.%m.%Y")
    return date_obj.strftime("%Y-%m-%d")

def time_to_seconds(t):
                h, m, s = t.split(':')
                return int(h)*3600 + int(m)*60 + float(s)


class WorkTimerWindow(QWidget):
    switch_to_stats = pyqtSignal()
    update_plot = pyqtSignal(float)

    def __init__(self):
        super().__init__()

        self.current_view = "w"

        self.data = db.get_all_data()
        
        starting_time = "00:00:00.00"
        previous_data_found = False

        for i in self.data:
            if i[0] == QDate.currentDate().toString("yyyy-MM-dd"):
                starting_time = i[1]
                previous_data_found = True


        self.time_label = QLabel(starting_time, self)
        self.date_label = QLabel(self)
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.reset_button = QPushButton("Reset", self)
        self.stats_button = QPushButton("Stats", self)

        self.initUI()

        self.timer = QTimer(self)
        
        if not previous_data_found:
            self.elapsed_time = QTime(0, 0, 0, 0)
        else:
            hours_str, minutes_str, sec_csec_str = starting_time.split(':')
            seconds_str, centiseconds_str = sec_csec_str.split('.')
            self.elapsed_time = QTime(int(hours_str), int(minutes_str), int(seconds_str), int(centiseconds_str) * 10)
            
        self.timer.timeout.connect(self.update_display)

        self.date_timer = QTimer(self)
        self.date_timer.timeout.connect(self.update_date_and_db)
        self.date_timer.start(1000)
        self.update_date_and_db()

        


    def initUI(self):
        self.setWindowTitle("work-timer")

        self.date_label.setText(QDate.currentDate().toString("d.M.yyyy"))
        self.stop_button.setEnabled(False)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        vbox.addWidget(self.date_label)
        vbox.addSpacing(40)

        self.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 18px;
            }
        """)

        hbox = QHBoxLayout()
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.reset_button)

        vbox.addLayout(hbox)
        vbox.addWidget(self.stats_button)
        vbox.setSpacing(2)

        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 48px; margin-bottom: 0px;")

        self.date_label.setAlignment(Qt.AlignVCenter)
        self.date_label.setAlignment(Qt.AlignLeft)
        self.date_label.setStyleSheet("font-size: 18px; margin-top: 0px;")

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)
        
         
        self.setLayout(vbox)

        self.stats_button.clicked.connect(self.switch_to_stats.emit)


    def change_view(self):
            if self.current_view == "w":
                self.current_view = "s"
                self.update_plot.emit(time_to_seconds(self.time_label.text()))
            else:
                self.current_view = "w"
            return


    def start(self):
        self.timer.start(10)
        self.stop_button.setEnabled(True)
        self.start_button.setEnabled(False)

    def stop(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        db.log_time(format_date(self.date_label.text()), self.time_label.text())

    def reset(self):
        self.timer.stop()
        self.elapsed_time = QTime(0, 0, 0, 0)
        self.time_label.setText(self.format_time(self.elapsed_time))
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        db.log_time(format_date(self.date_label.text()), self.time_label.text())
        self.update_plot.emit(time_to_seconds(self.time_label.text()))

    def format_time(self, time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        centiseconds = time.msec() // 10
        return f"{hours:02}:{minutes:02}:{seconds:02}.{centiseconds:02}"
        
    def update_display(self):
        self.elapsed_time = self.elapsed_time.addMSecs(10)
        self.time_label.setText(self.format_time(self.elapsed_time))
        
    def update_date_and_db(self):
        db.log_time(format_date(self.date_label.text()), self.time_label.text())
        old_date = self.date_label.text()
        if old_date != QDate.currentDate().toString("d.M.yyyy"):
            started = self.timer.isActive()
            self.reset()
            if started:
                self.start()
        self.date_label.setText(QDate.currentDate().toString("d.M.yyyy"))
        if self.current_view == "s":

            self.update_plot.emit(time_to_seconds(self.time_label.text()))






