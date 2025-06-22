import sys
from PyQt5.QtWidgets import QApplication
from view_controller import ViewController

def main():
    app = QApplication(sys.argv)
    window = ViewController()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()