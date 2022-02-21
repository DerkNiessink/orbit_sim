# Orbit sim

Application for simulating gravity between bodies with Newton's law of universal gravitation.

## Installation

1. Clone the repository.
1. [Create a virtual environment and activate it](https://docs.python.org/3/library/venv.html).
1. Install the requirements: `pip install -r requirements.txt`
1. Start the sim: `python orbit.py`

## Constellations

The constellations that Orbit sim can simulate are defined in JSON files. See the constellations folder for examples. 

If `orbit.py` is started without argument, it uses `constellations/first_constellation.json`. To specify a different consellation, pass the filename as argument: `python orbit.py constellations/constellation2.json`.

