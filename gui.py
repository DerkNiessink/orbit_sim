from multiprocessing import Process
import sys
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
import qdarktheme
import numpy as np
import json

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
            
        self.example_constellations = [filename.strip(".json") for filename in os.listdir("constellations") if ".json" in filename]
        self.conversion = Conversion(self.tableWidget, self.const_ComboBox)
        self.start_PushButton.clicked.connect(self.start_orbit)
        self.const_ComboBox.addItems(self.example_constellations)
        self.const_ComboBox.currentTextChanged.connect(self.show_current_constellation)
        self.const_ComboBox.textActivated.connect(self.make_uneditable)
        self.show_current_constellation()
        self.set_header()
        self.add_PushButton.clicked.connect(self.add_body)
        self.add_const_PushButton.clicked.connect(self.add_constellation)
        self.tableWidget.itemChanged.connect(self.conversion.table_to_json)
        self.delete_PushButton.clicked.connect(self.delete_body)

    def start_orbit(self):
        p = Process(target=orbit_sim, args=(f"./constellations/{self.const_ComboBox.currentText()}.json",))
        p.start()

    def show_current_constellation(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.set_header()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setColumnWidth(1, 150)
        if self.const_ComboBox.currentText() in self.example_constellations:
            self.make_uneditable()

            constellation = self.conversion.open_current_constellation()
            self.const_to_table(constellation)

    def const_to_table(self, constellation) -> None:
        """add the constellation items to the table"""
        for name, body in constellation["Constellation"].items():
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
        self.const_ComboBox.setEditable(False)

    def add_constellation(self) -> None:
        self.const_ComboBox.setEditable(True)
        self.const_ComboBox.setInsertPolicy(self.const_ComboBox.InsertAtTop)
        self.const_ComboBox.setCurrentIndex(0)

    def addItem(self, input) -> None:
        """add an item to the current column"""
        self.column += 1
        self.tableWidget.setItem(0, self.column, QTableWidgetItem(f"{input}"))

    def set_header(self) -> None:
        self.tableWidget.setHorizontalHeaderLabels(["Name" ,"Position (AU)", "Velocity (km/s)", "Radius (km)", "Mass (kg)", "Type", "Tail Length (px)"])

    def delete_body(self) -> None:
        """delete the selected body from the table and json file"""

        constellation = self.conversion.open_current_constellation()

        # delete current body in dict (if exists)
        if self.tableWidget.item(self.tableWidget.currentRow(), 0) != None:
            del constellation["Constellation"][f"{self.tableWidget.item(self.tableWidget.currentRow(), 0).text()}"]

        # delete current body in table
        self.tableWidget.removeRow(self.tableWidget.currentRow())
        self.conversion.save_constellation(constellation)



class Conversion:
    """Class for converting and saving the table as a json file"""

    def __init__(self, table, comboBox):
        self.table = table
        self.comboBox = comboBox

    def save_constellation(self, constellation) -> None:
        """save dict as json file"""
        with open(f"./constellations/{self.comboBox.currentText()}.json", "w") as fp:
            json.dump(constellation, fp, indent = 4)

    def open_current_constellation(self) -> None:
        """open json file as dict"""
        with open(f"./constellations/{self.comboBox.currentText()}.json") as json_file:
            return json.load(json_file)

    def table_to_json(self) -> None:
        """if updated, save data in table as json file"""

        # Check if all columns are filled
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                if self.table.item(row, column) == None:
                    return

        constellation = dict(Constellation=dict())

        # add items to constellations dict
        for row in range(self.table.rowCount()):
            body = {}
            for column in range(1, self.table.columnCount()):
                body[f"{self.table.horizontalHeaderItem(column).text()}"] = str(self.table.item(row, column).text())
            constellation["Constellation"][f"{self.table.item(row, 0).text()}"] = body

        self.convert_to_data(constellation["Constellation"])

        constellation["scale_factor"] = 10/AU
        constellation["time_step"] = 1800

        self.save_constellation(constellation)

    def convert_to_data(self, constellation):
        """Convert the constellation dict to a json file that can be used for the simulation"""

        new_keys = {"Position (AU)": "init_position", "Velocity (km/s)": "init_velocity", "Radius (km)": "radius", "Mass (kg)": "mass", "Type": "type", "Tail Length (px)": "tail length"}
        for body in constellation:
            # Check if the body is in the json format
            if not self.converted(constellation[body], new_keys):

                # Convert the body property keys to json keys
                constellation[body] = dict((new_keys[key], value) for (key, value) in constellation[body].items())

                # Convert the string properties of the body to json data
                self.string_to_data(constellation[body])

    def string_to_data(self, body_data):
        """Convert the strings to data that can be stored in the json file"""

        # Convert to list of floats with unit meters
        body_data["init_position"] = [val*AU for val in self.string_to_list(body_data["init_position"])]

        # Convert to list of floats with unit m/s
        body_data["init_velocity"] = [val*1000 for val in self.string_to_list(body_data["init_velocity"])]

        # Convert to float with unit meters
        body_data["radius"] = float(body_data["radius"]) * 1000

        body_data["mass"] = float(body_data["mass"])
        body_data["tail length"] = int(body_data["tail length"])

    def string_to_list(self, string):
        """Convert string of a tuple to list"""
        string = string.replace("(", "")
        string = string.replace(")", "")
        return [float(value) for value in list(string.split(","))]

    def converted(self, body_data, new_keys):
        """Check if the body is already converted to json data"""
        for key in new_keys:
            data = body_data.get(key, "not found")
            if data == "not found":
                return True
        return False


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