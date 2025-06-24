import sys
from PyQt5.QtWidgets import QApplication
from view_controller import ViewController
from db import init_db

def main():
    init_db()
    app = QApplication(sys.argv)
    window = ViewController()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()