from multiprocessing import Process
import sys
import os
from functools import partial

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem, QComboBox, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox
import qdarktheme
import numpy as np
import math

from sim import orbit_sim
from resources.image_type import images
from conversion import Conversion

AU = 149_597_871 * 10**3


class OrbitSimGui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.column = 0
        uic.loadUi(
            open("orbit_sim.ui"),
            self,
        )

        # Load in the names of the saved constellations in the resources repository
        self.constellations = [
            filename.strip(".json") for filename in os.listdir("constellations") if ".json" in filename
        ]

        self.conversion = Conversion(self.tableWidget, self.const_ComboBox)

        # Make dict for the type-ComboBoxes per constellation
        self.types_ComboBoxes = {}
        for constellation in self.constellations:
            self.types_ComboBoxes[constellation] = {}

        # Slots and signals
        self.start_PushButton.clicked.connect(self.start_sim)
        self.const_ComboBox.addItems(self.constellations)
        self.const_ComboBox.currentTextChanged.connect(self.show_current_constellation)
        self.show_current_constellation()
        self.set_header()
        self.add_PushButton.clicked.connect(self.add_body)
        self.add_const_PushButton.clicked.connect(self.add_constellation)
        self.tableWidget.itemChanged.connect(partial(self.conversion.table_to_json, self.types_ComboBoxes))
        self.delete_PushButton.clicked.connect(self.delete_body)
        self.delete_const_PushButton.clicked.connect(self.delete_constellation)

    def start_sim(self):
        """Start the simulation"""
        p = Process(target=orbit_sim, args=(f"./constellations/{self.const_ComboBox.currentText()}.json",))
        p.start()

    def show_current_constellation(self):
        """Show the selected constelllation in the table"""
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.set_header()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setColumnWidth(1, 125)
        self.tableWidget.setColumnWidth(5, 125)
        if self.const_ComboBox.currentText() in self.constellations:
            self.make_uneditable()
            constellation = self.conversion.open_current_constellation()
            self.const_to_table(constellation)

    def const_to_table(self, constellation) -> None:
        """add the constellation items to the table"""

        # Iterate over reversed dict, so that order of the table stays the same
        for name, body in reversed(constellation["Constellation"].items()):
            self.column = 0

            # determine if user input was orbital elements or cartesian
            init_position = body.get("init_position")
            init_velocity = body.get("init_velocity")
            if init_position == None:
                init_position, init_velocity = elements_to_cartesian(
                    body["aphelion"], body["min_orbital_velocity"], body["inclination"]
                )

            # add body parameters to columns
            self.add_body()
            self.addItem(name)
            self.addItem(tuple([round(x / AU, 2) for x in init_position]))
            self.addItem(tuple([round(x / 1000, 2) for x in init_velocity]))
            self.addItem(round(body["radius"] / 1000))
            self.addItem(scientific(body["mass"]))
            self.types_ComboBoxes[self.const_ComboBox.currentText()][self.tableWidget.rowCount()].setCurrentText(
                body["type"]
            )
            self.column += 1
            self.addItem(body.get("tail_length", 5000))

    def add_body(self) -> None:
        """Add an empty (except types-combobox) row to the table"""
        self.tableWidget.insertRow(0)
        self.addTypes()

    def make_uneditable(self) -> None:
        self.const_ComboBox.setEditable(False)
        self.types_ComboBoxes[self.const_ComboBox.currentText()] = {}

    def add_constellation(self) -> None:
        """Add an empty constellation to the constellations combobox"""
        self.const_ComboBox.setEditable(True)
        self.const_ComboBox.setInsertPolicy(self.const_ComboBox.InsertAtTop)

    def delete_constellation(self) -> None:
        """Delete a constellation from the constellations combobox and json file"""

        button = QMessageBox.question(
            self, "Confirm", f'Are you sure you want to delete "{self.const_ComboBox.currentText()}"?'
        )
        if button == QMessageBox.Yes:
            self.conversion.delete_constellation()
            self.const_ComboBox.removeItem(self.const_ComboBox.currentIndex())

    def addTypes(self) -> None:
        """Add the combobox containing the body types to column 5"""
        index = self.tableWidget.rowCount()
        constellation = self.const_ComboBox.currentText()
        self.types_ComboBoxes[constellation][index] = QComboBox()
        self.types_ComboBoxes[constellation][index].addItems([key for key in images])
        self.types_ComboBoxes[constellation][index].currentTextChanged.connect(
            partial(self.conversion.table_to_json, self.types_ComboBoxes)
        )
        self.tableWidget.setCellWidget(0, 5, self.types_ComboBoxes[constellation][index])

    def addItem(self, input) -> None:
        """add an item to the current column"""
        self.tableWidget.setItem(0, self.column, QTableWidgetItem(f"{input}"))
        self.column += 1

    def set_header(self) -> None:
        self.tableWidget.setHorizontalHeaderLabels(
            ["Name", "Position (AU)", "Velocity (km/s)", "Radius (km)", "Mass (kg)", "Type", "Tail Length (px)"]
        )

    def delete_body(self) -> None:
        """delete the selected body from the table and json file"""

        constellation = self.conversion.open_current_constellation()

        # delete current body in dict (if exists)
        if self.tableWidget.item(self.tableWidget.currentRow(), 0) != None:
            del constellation["Constellation"][f"{self.tableWidget.item(self.tableWidget.currentRow(), 0).text()}"]

        # delete current body in table
        self.tableWidget.removeRow(self.tableWidget.currentRow())
        self.conversion.save_constellation(constellation)


def scientific(input) -> str:
    return np.format_float_scientific(input, precision=2)


def elements_to_cartesian(aphelion, min_orbital_velocity, inclination) -> tuple:
    # convert orbital elements to cartesian position and velocity vectors
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
