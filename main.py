import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import MainWindow

class AntivirusApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("极速云杀毒")
        self.setApplicationVersion("1.0.0")
        
    def run(self):
        main_window = MainWindow()
        main_window.show()
        return self.exec_()

if __name__ == "__main__":
    app = AntivirusApp(sys.argv)
    sys.exit(app.run())
