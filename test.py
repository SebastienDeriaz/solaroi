import numpy as np
from solaroi import Solaroi

consumption = np.array([100, 100, 100, 100])
production = np.array([100, 200, 100, 100])
battery_capacity = 100
max_battery_charge = 10
max_battery_discharge = 10
efficiency = 1

def main():
    s = Solaroi()
    s.load(consumption, production, 3600)
    grid, storage = s.run(battery_capacity, max_battery_charge, max_battery_discharge, efficiency)

    print(f"Grid : {grid}")
    print(f"Storage : {storage}")



if __name__ == '__main__':
    main()