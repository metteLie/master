
# Floating PV System Simulation

This project simulates the performance of Floating Photovoltaic (FPV) systems on various lakes. It includes modules for setting up PV systems, simulating energy yield, and handling environmental factors like soiling losses.

## Project Structure

```
├── pvmodel.py
├── pvsystem.py
├── simulation.py
├── soiling_loss_NS3031.py
├── lake.py
├── data/
│   ├── raw_data/
│   └── processed_data/
├── venv/
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/metteLie/master.git
```

2. Navigate to the project directory:

```bash
cd master
```

3. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Simulation of Annual Energy Yield

The `simulation.py` module contains the `FPVsimulation` class that allows you to simulate the annual energy yield of multiple FPV systems.

#### Example Usage

```python
from simulation import FPVsimulation

# Create an instance of FPVsimulation
sim = FPVsimulation()

# Set custom PV model parameters if needed
custom_params = {
    'eff_nom': 20,  # Nominal efficiency
    'tau': 0.9,
    'alpha': 0.05,
    'U': 25,
    'system_derate_factor': 0.8
}
sim.set_PVmodel_parameters(custom_params)

# Register lakes and their PV systems using a DataFrame
lakes_df = pd.read_csv('path_to_lakes_data.csv')
sim.register_lakes(lakes_df)

# Get the annual energy yield for all registered lakes
annual_yield_df = sim.get_annual_energy_yield()

# Save the results to an Excel file
sim.get_annual_energy_yield_xlsx('annual_energy_yield')
```
### Documentation

Inside `docs/` the `.rst` files contain additional descriptions
of the module and its components, as well as pulling in docstrings from the module source.
Build the docs using
```shell
cd docs
sphinx-build -b html source build/html
cd build/html
start index.html 
```

### Building

Build the python package using
```shell
pip install build
python -m build
pip install -e .
```

### Project structure
- **`src/areaSelection`**: The method for selecting lake areas for FPV simulation, creates csv files: gross_area_systems, social_area_systems, social_area_2km_systems, practical_systems and hydro_power_systems.
- **`src/FPVsimulation`**: The FPVsimulation Python module, containing the core source.


### Modules Description

- **`pvmodel.py`**: Contains the `PVmodel` class, which simulates the performance of a simple photovoltaic module.
- **`pvsystem.py`**: Contains the `PVsystem` class, which represents a PV system and its simulation methods.
- **`simulation.py`**: Contains the `FPVsimulation` class, which manages multiple lakes and their PV systems.
- **`lake.py`**: Contains the `Lake` class, which represents a lake with PV systems and calculates their energy yield.
- **`soiling_loss_NS3031.py`**: Contains data and methods for calculating soiling losses based on geographical locations.

### Data Directory

- **`data/raw_data/`**: Directory to store raw data files.
- **`data/processed_data/`**: Directory to store processed data files.

## License

This project is licensed under the MIT License.
