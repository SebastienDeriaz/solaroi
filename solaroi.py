import numpy as np


class Solaroi:
    def __init__(self) -> None:
        pass

    def load(self, consumption, production, dt):
        """
        consumption [Wh]
        production [Wh]
        dt [s]
        """
        self._dt = dt
        self._consumption = consumption # Wh
        self._production = production # Wh


    def run(self, battery_capacity, battery_max_charge, battery_max_discharge, battery_efficiency):
        """
        battery_capacity [Wh]
        battery_max_charge [W]
        battery_max_discharge [W]
        battery_efficiency [-] (roundtrip)
        """
        grid_consumption = []
        battery_storage = []
        current_battery_storage = 0 # Wh
        for ic, ip in zip(self._consumption, self._production):
            if ic > ip:
                # If consumption is higher than product, discharge the battery
                battery_energy_delta = -min(battery_max_discharge*self._dt/3600, ic-ip, current_battery_storage * battery_efficiency)
            elif ic < ip:
                # If consumption is lower than production, charge the battery
                battery_energy_delta = min(battery_max_charge*self._dt/3600, ip-ic, battery_capacity-current_battery_storage)

            grid_consumption.append(ic - ip - battery_energy_delta)
            current_battery_storage += battery_energy_delta * battery_efficiency
            battery_storage.append(current_battery_storage)

        return grid_consumption, battery_storage




