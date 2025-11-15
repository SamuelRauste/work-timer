from PyQt5.QtWidgets import QWidget, QStackedLayout, QSizePolicy
from views import WorkTimerWindow, StatsWindow
from PyQt5.QtGui import QIcon
import sys, os

# class for managing the view that is visible to the user

class ViewController(QWidget):
    def __init__(self):
        super().__init__()

        def resource_path(relative_path):
            if hasattr(sys, "_MEIPASS"):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        icon_path = resource_path("favicon.ico")
        self.setWindowIcon(QIcon(icon_path))



        self.setWindowTitle("work-timer")

        self.work_timer_view = WorkTimerWindow()
        self.stats_view = StatsWindow()

        self.work_timer_view.update_plot.connect(self.stats_view.draw_plot)

        self.view_stack = QStackedLayout()
        self.view_stack.addWidget(self.work_timer_view)
        self.view_stack.addWidget(self.stats_view)
        self.setLayout(self.view_stack)

        self.view_stack.setCurrentWidget(self.work_timer_view)
        self.setFixedSize(self.work_timer_view.sizeHint())

        self.work_timer_view.switch_to_stats.connect(lambda: self.change_view(self.stats_view))
        self.stats_view.switch_to_timer.connect(lambda: self.change_view(self.work_timer_view))

    def change_view(self, view):
        self.view_stack.setCurrentWidget(view)
        self.setFixedSize(view.sizeHint())
        self.work_timer_view.change_view()


