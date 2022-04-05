from PyQt5 import QtWidgets, uic

from multiprocessing import Process
import threading
import sys
from orbit import orbit_sim


class OrbitSimGui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi(
            open("orbit_sim.ui"),
            self,
        )

        self.start_PushButton.clicked.connect(self.start_orbit)
        self.constellation_ComboBox.addItems(["Solar", "Inclined", "Binary"])

    def start_orbit(self, event):
        p = Process(target=orbit_sim, args=(f"constellations.{self.constellation_ComboBox.currentText()}",))
        p.start()

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = OrbitSimGui()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()