import time
import numpy as np
from badger import environment
from badger.interface import Interface



class Environment(environment.Environment):

    name = 'petraIII_injection'

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)

        # mapping from badger addresses to tine addresses 
        self.channel_to_tine_params = {var: ("/".join(var.split('/')[:-1]), 
                                             var.split('/')[-1]) for var in self.list_vars() + self.list_obses()
                                             }
        self.init_values = {channel : self._get_var(channel) for channel in self.list_vars()}

    def boundaries_rel_to_init_val(self, channel: str, interval: float):
        return [self.init_values[channel] - interval, self.init_values[channel] + interval]
    
    def _get_vrange(self, var):

        return {"PETRA/Cms.MagnetPs/QF/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/QF/Strom.Soll", 5),
                "PETRA/Cms.MagnetPs/QD/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/QD/Strom.Soll", 5),
                "PETRA/Kicker/Septum_Inj/FO_Soll": self.boundaries_rel_to_init_val("PETRA/Kicker/Septum_Inj/FO_Soll", 5),
                "PETRA/Cms.MagnetPs/IME186/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/IME186/Strom.Soll", 1),
                "PETRA/Cms.MagnetPs/SHE183/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/SHE183/Strom.Soll", 1),
                "PETRA/Cms.MagnetPs/SVE189/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/SVE189/Strom.Soll", 1),
                "PETRA/Cms.MagnetPs/SVE188/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/SVE188/Strom.Soll", 1),
                "PETRA/Cms.MagnetPs/SVE178/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/SVE178/Strom.Soll", 1),
                "PETRA/Cms.MagnetPs/SVE170/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/SVE170/Strom.Soll", 1),
                }[var]

    @staticmethod
    def list_vars():
        return ["PETRA/Cms.MagnetPs/QF/Strom.Soll",
                "PETRA/Cms.MagnetPs/QD/Strom.Soll",
                "PETRA/Kicker/Septum_Inj/FO_Soll",
                "PETRA/Cms.MagnetPs/IME186/Strom.Soll",
                "PETRA/Cms.MagnetPs/SHE183/Strom.Soll",
                "PETRA/Cms.MagnetPs/SVE189/Strom.Soll",
                "PETRA/Cms.MagnetPs/SVE188/Strom.Soll",
                "PETRA/Cms.MagnetPs/SVE178/Strom.Soll",
                "PETRA/Cms.MagnetPs/SVE170/Strom.Soll",
                ]

    @staticmethod
    def list_obses():
        return ['PETRA/Transfers/#0/Efficiency.Desy2Petra']

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


        if obs == 'PETRA/Transfers/#0/Efficiency.Desy2Petra':
            tine_channel, prop = self.channel_to_tine_params[obs]
            val = self.interface.get_value(tine_channel, prop)
            return val

        raise NotImplementedError(f"obs {obs} is not implemented.")
    
if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(1, os.getcwd() + '/interfaces')
    from tine import Interface

    print("Start Test...")
    petra = Environment(Interface(), None)

    var = petra._get_obs('PETRA/Transfers/#0/Efficiency.Desy2Petra')
    print(f"PETRA/Transfers/#0/Efficiency.Desy2Petra : {var}")