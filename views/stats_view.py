from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget
from PyQt5.QtCore import Qt, QTimer, QTime, QDate, pyqtSignal
import db

# The view where statistics will be displayed

class StatsWindow(QWidget):
    switch_to_timer = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.label = QLabel("STATSVIEW", self)
        self.label.setStyleSheet("font-size: 48px;")
        self.work_timer_view_btn = QPushButton("Timer", self)

        self.list_widget = QListWidget()
        self.data = db.get_all_data()
        for i in self.data:
            self.list_widget.addItem(i[0] + "   " + i[1])

        self.list_widget.setFixedHeight(100)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.list_widget)
        vbox.addWidget(self.work_timer_view_btn)
        self.setLayout(vbox)

        self.work_timer_view_btn.clicked.connect(self.switch_to_timer)

