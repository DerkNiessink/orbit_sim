from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QCoreApplication
import pkg_resources
import threading
import sys
from orbit import orbit_sim


class OrbitSimGui(QtWidgets.QMainWindow):
    
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        uic.loadUi(
            open("orbit_sim.ui"),
            self,
        )

        self.start_button.clicked.connect(self.start_orbit)

    def start_orbit(self, event):
        self.thread = threading.Thread(target=orbit_sim)
        self.thread.start()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = OrbitSimGui()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()