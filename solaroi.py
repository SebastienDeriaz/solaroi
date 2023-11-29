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
        battery_efficiency [-] (single trip)
        """
        self.grid_consumption = []
        self.battery_storage = []
        self.auto_consumption = []
        self.energy_stored = []
        self.energy_released = []
        current_battery_storage = 0 # Wh

        

        for ic, ip in zip(self._consumption, self._production):
            delta = ic - ip # >0 consumption, <0 production
            
            battery_energy_delta = min(max(-battery_max_discharge*self._dt/3600, -delta, -current_battery_storage), battery_capacity-current_battery_storage, battery_max_charge*self._dt/3600)

            self.grid_consumption.append(delta + battery_energy_delta)
            self.auto_consumption.append(min(ic, ip))
            if battery_energy_delta < 0:
                # Discharging
                current_battery_storage += battery_energy_delta / battery_efficiency
                self.energy_stored.append(0)
                self.energy_released.append(-battery_energy_delta)
            else:
                # Charging
                current_battery_storage += battery_energy_delta * battery_efficiency
                self.energy_stored.append(battery_energy_delta)
                self.energy_released.append(0)           
            
            self.battery_storage.append(current_battery_storage)

        self.grid_consumption = np.array(self.grid_consumption)
        self.battery_storage = np.array(self.battery_storage)
        return self.grid_consumption, self.battery_storage


    def report(self, kwh_buy, kwh_sell):
        output = {
            'kwh_buy' : kwh_buy,
            'kwh_sell' : kwh_sell,
            'production' : np.sum(self._production),
            'consumption' : np.sum(self._consumption),
            'auto_consumption' : np.sum(self.auto_consumption),
            'energy_stored' : np.sum(self.energy_stored),
            'energy_released' : np.sum(self.energy_released),
            'grid_positive' : np.sum(self.grid_consumption[self.grid_consumption > 0]),
            'grid_negative' : -np.sum(self.grid_consumption[self.grid_consumption < 0]),
            'grid_total' : np.sum(self.grid_consumption)
        }
        return output

    def print_report(self, report):
        print(f"Production            : {report['production']/1e6:7.3f} MWh")
        print(f"Consumption           : {report['consumption']/1e6:7.3f} MWh")
        print(f"  Auto-consumption    : {report['auto_consumption']/1e6:7.3f} MWh ({report['auto_consumption']/1e3*report['kwh_buy']:7.2f} CHF)")
        print(f"  From Battery        : {report['energy_released']/1e6:7.3f} MWh ({report['energy_released']/1e3*report['kwh_buy']:7.2f} CHF)")
        print(f"  From grid           : {report['grid_positive']/1e6:7.3f} MWh ({report['grid_positive']/1e3*report['kwh_buy']:7.2f} CHF)")
        print(f"Grid sell             : {report['grid_negative']/1e6:7.3f} MWh ({report['grid_negative']/1e3*report['kwh_sell']:7.2f} CHF)")
        print(f"Grid total            : {report['grid_total']/1e6:+7.3f} MWh ({report['grid_negative']/1e3*report['kwh_sell'] + report['grid_positive']/1e3*report['kwh_buy']:7.2f} CHF)")
            










