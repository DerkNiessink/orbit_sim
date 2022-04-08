from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

from multiprocessing import Process
import sys
from orbit import orbit_sim
import qdarktheme
import importlib
import numpy as np
import math
from resources.image_type import images

AU = 149_597_871 * 10 ** 3


class OrbitSimGui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.column = 0
        uic.loadUi(
            open("orbit_sim.ui"),
            self,
        )
        
        
        self.start_PushButton.clicked.connect(self.start_orbit)
        self.constellation_ComboBox.addItems(["Custom", "Inclined", "Solar", "Binary"])
        self.constellation_ComboBox.currentTextChanged.connect(self.show_example)
        self.constellation_ComboBox.activated.connect(self.show_example)
        self.add_PushButton.clicked.connect(self.add_body)


    def start_orbit(self):
        p = Process(target=orbit_sim, args=(f"constellations.{self.constellation_ComboBox.currentText()}",))
        p.start()

    def show_example(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        if self.constellation_ComboBox.currentText() != "Custom":    
            constellation = importlib.import_module(f".{self.constellation_ComboBox.currentText()}", "constellations")
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(["Name" ,"Position (AU)", "Velocity (km/s)", "Radius (km)", "Mass (kg)", "Type", "Tail Length (px)"])
            self.tableWidget.setColumnWidth(1, 130)
            self.const_to_table(constellation.constellation)

    def const_to_table(self, constellation):
        for name, body in constellation.items():
            self.column = 0
            self.tableWidget.insertRow(0)
            self.tableWidget.setItem(0, 0, QTableWidgetItem(name))
            init_position = body.get("init_position")
            init_velocity = body.get("init_velocity")
            if init_position == None:
                init_position, init_velocity = elements_to_cartesian(body["aphelion"], body["min_orbital_velocity"], body["inclination"])

            self.addItem(tuple([round(x/AU, 2) for x in init_position]))
            self.addItem(tuple([round(x/1000,2) for x in init_velocity]))
            self.addItem(round(body["radius"]/1000))
            self.addItem(scientific(body["mass"]))
            self.addItem(body["type"])
            self.addItem(body.get("tail_length", 5000))

    def add_body(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        

    def addItem(self, input):
        self.column += 1
        self.tableWidget.setItem(0, self.column, QTableWidgetItem(f"{input}"))

def scientific(input):
    return np.format_float_scientific(input, precision = 2)


def elements_to_cartesian(aphelion, min_orbital_velocity, inclination): 
    inclination_rad = math.radians(inclination)
    position = (aphelion * math.cos(inclination_rad), 0, aphelion * math.sin(inclination_rad))
    velocity = (0, min_orbital_velocity, 0)
    return position, velocity


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    ui = OrbitSimGui()
    ui.show()
    sys.exit(app.exec())
    

if __name__ == "__main__":
    main()