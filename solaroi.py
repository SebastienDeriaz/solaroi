import numpy as np


class Solaroi:
    def __init__(self) -> None:
        pass

    def load(self, time, consumption, production):
        self._time = time # Time vector [s]
        self._consumption = consumption # Wh
        self._production = production # Wh