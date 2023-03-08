import time
import numpy as np
from badger import environment
from badger.interface import Interface



class Environment(environment.Environment):

    name = 'petraIII_skew_quads'

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)

        # mapping from badger addresses to tine addresses 
        self.channel_to_tine_params = {var: ("/".join(var.split('/')[:-1]), 
                                             var.split('/')[-1]) for var in self.list_vars() + self.list_obses()
                                             }

        self.init_currents_of_mag = [self._get_var(mag) for mag in self.list_vars()]

    def _get_vrange(self, var):
        return {mag_name: [curr_val -5, curr_val + 5] for mag_name, curr_val in zip(self.list_vars(), self.init_currents_of_mag)}[var]
    
    @staticmethod
    def list_vars():
        return ["PETRA/Cms.MagnetPs/QS_W1/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_W2/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_W3/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_W4/Strom.Soll", 
                "PETRA/Cms.MagnetPs/QS_N1/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_N2/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_N3/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_N4/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_NO1/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_NO2/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_O3/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_O4/Strom.Soll"]

    @staticmethod
    def list_obses():
        return ['PETRA/Lifetime/#0/Tau']

    @staticmethod
    def get_default_params():
        return {
            'waiting_time': 1,
        }

    def _get_var(self, var):
        tine_channel, prop = self.channel_to_tine_params[var]
        # print(f"tine_channel: {tine_channel}")
        # print(f"prop: {prop}")
        return self.interface.get_value(tine_channel, prop)

    def _set_var(self, var, x):
        tine_channel, prop = self.channel_to_tine_params[var]
        self.interface.set_value(tine_channel, prop, x)

    def _get_obs(self, obs):
        time.sleep(self.params.get('waiting_time', 0))


        if obs == "PETRA/Lifetime/#0/Tau":
            tine_channel, prop = self.channel_to_tine_params[obs]
            val = self.interface.get_value(tine_channel, prop) # returns a list with three elements (e.g [8.410006523132324, 8.410006523132324, 15.865203857421875])
            return val[0]

        raise NotImplementedError(f"obs {obs} is not implemented.")
    