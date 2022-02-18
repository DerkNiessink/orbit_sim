from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
import sys
import pkg_resources


pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class OrbitController(QtWidgets.QMainWindow):
    def __init__(self):

        super().__init__()

        uic.loadUi(
            pkg_resources.resource_stream("resources", "orbit.ui"),
            self,
        )


def run_gui():
    app = QtWidgets.QApplication(sys.argv)
    ui = OrbitController()
    ui.show()
    sys.exit(app.exec())
