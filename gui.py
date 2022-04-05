from PyQt5 import QtWidgets, uic

from multiprocessing import Process
import sys
from orbit import orbit_sim
import qdarktheme



class OrbitSimGui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi(
            open("orbit_sim.ui"),
            self,
        )

        self.start_PushButton.clicked.connect(self.start_orbit)
        self.constellation_ComboBox.addItems(["Solar", "Inclined", "Binary"])
        self.example_PushButton.clicked.connect(self.show_example)

    def start_orbit(self):
        p = Process(target=orbit_sim, args=(f"constellations.{self.constellation_ComboBox.currentText()}",))
        p.start()

    def show_example(self):
        self.constellation_textEdit.clear()
        self.constellation_textEdit.setPlainText(f"{self.constellation_ComboBox.currentText()}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    ui = OrbitSimGui()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()