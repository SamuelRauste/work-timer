from PyQt5.QtWidgets import QWidget, QStackedLayout
from views import WorkTimerWindow

class ViewController(QWidget):
    def __init__(self):
        super().__init__()

        self.work_timer = WorkTimerWindow()

        view_stack = QStackedLayout()
        view_stack.addWidget(self.work_timer)
        self.setLayout(view_stack)