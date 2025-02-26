from flight_dynamics import FlightDynamicsModel
from visuals import Visuals
from hardware_interface import HardwareInterface
import threading
from utils import *

class Simulator:
    def __init__(self):
        self.fdm = FlightDynamicsModel()
        self.visuals = Visuals()
        self.hardware = HardwareInterface()

    def update_sim(self):
        while True:
            if self.hardware.mouse_enable:
                self.fdm.set_controls(self.visuals.aileron, self.visuals.elevator, self.visuals.throttle)
            else:
                aileron, elevator, throttle = self.hardware.read_inputs()
                self.fdm.set_controls(aileron, elevator, throttle)

            self.fdm.update()

            self.visuals.update_state(self.fdm.get_fdm()['attitude/phi-deg'], 
                                      self.fdm.get_fdm()['attitude/theta-deg'], 
                                      self.fdm.get_fdm()['attitude/psi-deg'], 
                                      self.fdm.get_fdm()['position/lat-geod-deg'],
                                      self.fdm.get_fdm()['position/long-gc-deg'],
                                      self.fdm.initial_lat,
                                      self.fdm.initial_lon,
                                      self.fdm.get_fdm()['position/h-sl-ft'] * 0.3048)

    def start(self):
        sim_thread = threading.Thread(target=self.update_sim)
        sim_thread.daemon = True
        sim_thread.start()

        self.visuals.run()

if __name__ == "__main__":
    sim = Simulator()
    sim.start()