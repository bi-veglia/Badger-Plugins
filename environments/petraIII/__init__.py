import time
import numpy as np
from scipy.optimize import curve_fit
from badger import environment
from badger.interface import Interface



class Environment(environment.Environment):

    name = 'petraIII'

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
    
        return {"PETRA/Cms.MagnetPs/QS1/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/QS1/Strom.Soll", 15),
                "PETRA/Cms.MagnetPs/QS2/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/QS2/Strom.Soll", 15),
                "PETRA/Cms.MagnetPs/QS3/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/QS3/Strom.Soll", 15),
                "PETRA/Cms.MagnetPs/QS4/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/QS4/Strom.Soll", 15),
                "PETRA/Cms.MagnetPs/QF/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/QF/Strom.Soll", 0.50),
                "PETRA/Cms.MagnetPs/QD/Strom.Soll": self.boundaries_rel_to_init_val("PETRA/Cms.MagnetPs/QD/Strom.Soll", 0.50),
                }[var]

    @staticmethod
    def list_vars():
        
        return ["PETRA/Cms.MagnetPs/QS1/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS2/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS3/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS4/Strom.Soll",
                "PETRA/Cms.MagnetPs/QF/Strom.Soll",
                "PETRA/Cms.MagnetPs/QD/Strom.Soll"]

    @staticmethod
    def list_obses():
        return ['Lifetime','Vertical_Emittance']
    

    @staticmethod
    def get_default_params():
        return {
            'waiting_time': 1,
            'lt_time_step': 1,
            'timerange': 20,
        }

    def _get_var(self, var):
        tine_channel, prop = self.channel_to_tine_params[var]
        return self.interface.get_value(tine_channel, prop)

    def _set_var(self, var, x):
        tine_channel, prop = self.channel_to_tine_params[var]
        self.interface.set_value(tine_channel, prop, x)

    def _get_obs(self, obs):
        print("Calling _get_obs")
        time.sleep(self.params.get('waiting_time', 1))

        if obs == "Lifetime":
            #to improve accuracy we need to be reading from this channel "/PETRA/idc/Buffer-0/Current" every second for ~20 seconds *possibly less
        #and fit an exp-function to the retrieved data: I(t)=I_0*exp(-t/tau)
        #add timerange as a user defined parameter in order to be adjusted
            timerange=self.params.get('timerange', 20)
            data=np.zeros((timerange))
            timestamp=np.zeros((timerange))
            for s in range(timerange):
                data[s], timestamp[s] = self.interface.get_value_with_timestamp("/PETRA/idc/Buffer-0","Current")
                time.sleep(self.params.get('lt_time_step', 1))
            # Fit the function a * np.exp(b * t) + c to x and y
            tau,_ = curve_fit(lambda t, tau: data[0] * np.exp(-t/tau), np.array(timestamp)-timestamp[0], data)
            return data[0]*tau[0]/3600
        

            
        if obs =="Vertical_Emittance":
            val = self.interface.get_value("PETRA/IfmDiagBeamData/Vertical","Vemittance") 
            return val

        raise NotImplementedError(f"obs {obs} is not implemented.")
