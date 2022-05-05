import json
import os

AU = 149_597_871 * 10 ** 3


class Conversion:
    """Class for converting and saving the table as a json file"""

    def __init__(self, table, ComboBox):
        self.table = table
        self.ComboBox = ComboBox

    def save_constellation(self, constellation) -> None:
        """save dict as json file"""
        with open(f"./constellations/{self.ComboBox.currentText()}.json", "w") as fp:
            json.dump(constellation, fp, indent = 4)

    def open_current_constellation(self) -> None:
        """open json file as dict"""
        with open(f"./constellations/{self.ComboBox.currentText()}.json") as json_file:
            return json.load(json_file)

    def delete_constellation(self) -> None:
        """delete current constellation json file"""
        try:
            os.remove(f"./constellations/{self.ComboBox.currentText()}.json")
        except:
            # Ignore error when constellation was added to combobox but not yet saved
            FileNotFoundError 

    def table_to_json(self, types_ComboBoxes) -> None:
        """if updated, save data in table as json file"""

        # Check if all columns are filled
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                if self.table.item(row, column) == None and column != 5:
                    return

        constellation = dict(Constellation=dict())

        # add items to constellations dict
        for row in range(self.table.rowCount()):
            body = {}
            for column in range(1, self.table.columnCount()):
                if self.table.horizontalHeaderItem(column).text() == "Type":
                    body["Type"] = types_ComboBoxes[self.ComboBox.currentText()][self.table.rowCount()-row].currentText() # rowCount - row because ComboBoxes were added in reverse order.
                else:
                    body[f"{self.table.horizontalHeaderItem(column).text()}"] = str(self.table.item(row, column).text())
            constellation["Constellation"][f"{self.table.item(row, 0).text()}"] = body

        self.convert_to_data(constellation["Constellation"])

        constellation["scale_factor"] = 10/ AU
        constellation["time_step"] = 1800

        self.save_constellation(constellation)

    def convert_to_data(self, constellation):
        """Convert the constellation dict to a json file that can be used for the simulation"""

        new_keys = {"Position (AU)": "init_position", "Velocity (km/s)": "init_velocity", "Radius (km)": "radius", "Mass (kg)": "mass", "Type": "type", "Tail Length (px)": "tail_length"}
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
        body_data["tail_length"] = int(body_data["tail_length"])

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