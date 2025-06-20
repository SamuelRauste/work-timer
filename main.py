import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QTime

class WorkTimerWindow(QWidget):
    def __init__(self):
        super().__init__()
        

        self.time_label = QLabel("00:00:00.00", self)
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.reset_button = QPushButton("Reset", self)

        self.timer = QTimer(self)
        self.elapsed_time = QTime(0, 0, 0, 0)

        self.initUI()

        

    def initUI(self):
        self.setWindowTitle("work-timer")
        

        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)

        hbox = QHBoxLayout()
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.reset_button)

        vbox.addLayout(hbox)

        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 48px;")

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)
        self.timer.timeout.connect(self.update_display)
         

        self.setLayout(vbox)

    def start(self):
        self.timer.start(10)

    def stop(self):
        self.timer.stop()

    def reset(self):
        self.timer.stop()
        self.elapsed_time = QTime(0, 0, 0, 0)
        self.time_label.setText(self.format_time(self.elapsed_time))

    def format_time(self, time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        milliseconds = time.msec() // 10
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}"
        

    def update_display(self):
        self.elapsed_time = self.elapsed_time.addMSecs(10)
        self.time_label.setText(self.format_time(self.elapsed_time))

        


    


        

def main():
    app = QApplication(sys.argv)
    window = WorkTimerWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()