import importlib
import math
from multiprocessing import Process
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
import qdarktheme
import numpy as np

from orbit import orbit_sim
from models.physicalobject import elements_to_cartesian



AU = 149_597_871 * 10 ** 3


class OrbitSimGui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.column = 0
        uic.loadUi(
            open("orbit_sim.ui"),
            self,
        )
        
        self.example_constellations = ["Solar", "Inclined", "Binary"]
        self.start_PushButton.clicked.connect(self.start_orbit)
        self.constellation_ComboBox.addItems(self.example_constellations)
        self.constellation_ComboBox.currentTextChanged.connect(self.show_current_constellation)
        self.constellation_ComboBox.textActivated.connect(self.make_uneditable)
        self.show_current_constellation()
        self.set_header()
        self.add_PushButton.clicked.connect(self.add_body)
        self.add_constellation_PushButton.clicked.connect(self.add_constellation)
        
    def start_orbit(self):
        p = Process(target=orbit_sim, args=(f"constellations.{self.constellation_ComboBox.currentText()}",))
        p.start()

    def show_current_constellation(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.set_header()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setColumnWidth(1, 130)
        if self.constellation_ComboBox.currentText() in self.example_constellations:  
            self.make_uneditable()
            constellation = importlib.import_module(f".{self.constellation_ComboBox.currentText()}", "constellations")
            self.const_to_table(constellation.constellation)
            

    def const_to_table(self, constellation) -> None:
        """add the constellation items to the table"""
        for name, body in constellation.items():
            self.column = 0
            self.tableWidget.insertRow(0)
            self.tableWidget.setItem(0, 0, QTableWidgetItem(name))

            # determine if user input was orbital elements or cartesian
            init_position = body.get("init_position")
            init_velocity = body.get("init_velocity")
            if init_position == None:
                init_position, init_velocity = elements_to_cartesian(body["aphelion"], body["min_orbital_velocity"], body["inclination"])

            # add body parameters to columns
            self.addItem(tuple([round(x/AU, 2) for x in init_position]))
            self.addItem(tuple([round(x/1000,2) for x in init_velocity]))
            self.addItem(round(body["radius"]/1000))
            self.addItem(scientific(body["mass"]))
            self.addItem(body["type"])
            self.addItem(body.get("tail_length", 5000))

    def add_body(self) -> None:
        self.tableWidget.insertRow(self.tableWidget.rowCount())

    def make_uneditable(self) -> None:
        self.constellation_ComboBox.setEditable(False)

    def add_constellation(self) -> None:
        self.constellation_ComboBox.setEditable(True)
        self.constellation_ComboBox.setInsertPolicy(self.constellation_ComboBox.InsertAtTop)
        self.constellation_ComboBox.setCurrentIndex(0)

    def addItem(self, input) -> None:
        # add an item to the current column
        self.column += 1
        self.tableWidget.setItem(0, self.column, QTableWidgetItem(f"{input}"))

    def set_header(self) -> None:
        self.tableWidget.setHorizontalHeaderLabels(["Name" ,"Position (AU)", "Velocity (km/s)", "Radius (km)", "Mass (kg)", "Type", "Tail Length (px)"])


def scientific(input) -> str:
    return np.format_float_scientific(input, precision = 2)

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    ui = OrbitSimGui()
    ui.show()
    sys.exit(app.exec())
    

if __name__ == "__main__":
    main()