import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QTime, QDate

class WorkTimerWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.time_label = QLabel("00:00:00.00", self)
        self.date_label = QLabel(self)
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.reset_button = QPushButton("Reset", self)

        self.timer = QTimer(self)
        self.elapsed_time = QTime(0, 0, 0, 0)

        self.date_timer = QTimer(self)
        self.date_timer.timeout.connect(self.update_date)
        self.date_timer.start(1000)
        self.update_date()

        self.initUI()


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

        vbox.setSpacing(2)

        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 48px; margin-bottom: 0px;")

        
        self.date_label.setAlignment(Qt.AlignVCenter)
        self.date_label.setAlignment(Qt.AlignLeft)
        self.date_label.setStyleSheet("font-size: 18px; margin-top: 0px;")

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)
        self.timer.timeout.connect(self.update_display)
         
        self.setLayout(vbox)


    def start(self):
        self.timer.start(10)
        self.stop_button.setEnabled(True)
        self.start_button.setEnabled(False)

    def stop(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def reset(self):
        self.timer.stop()
        self.elapsed_time = QTime(0, 0, 0, 0)
        self.time_label.setText(self.format_time(self.elapsed_time))
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def format_time(self, time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        milliseconds = time.msec() // 10
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}"
        

    def update_display(self):
        self.elapsed_time = self.elapsed_time.addMSecs(10)
        self.time_label.setText(self.format_time(self.elapsed_time))
        

    def update_date(self):

        old_date = self.date_label.text()
        if old_date != QDate.currentDate().toString("d.M.yyyy"):
            started = self.timer.isActive()
            if started:
                # Update database here later
                self.reset()
                self.start()
            else:
                # Update database here later
                self.reset()


        self.date_label.setText(QDate.currentDate().toString("d.M.yyyy"))

        

def main():
    app = QApplication(sys.argv)
    window = WorkTimerWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()