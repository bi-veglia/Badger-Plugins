import time
import numpy as np
from scipy.optimize import curve_fit
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
        return ['Lifetime','Vertical_Emittance']

    @staticmethod
    def get_default_params():
        return {
            'waiting_time': 1,
            'timerange': 20,
        }

    def _get_var(self, var):
        tine_channel, prop = self.channel_to_tine_params[var]
        return self.interface.get_value(tine_channel, prop)

    def _set_var(self, var, x):
        tine_channel, prop = self.channel_to_tine_params[var]
        self.interface.set_value(tine_channel, prop, x)

    def _get_obs(self, obs):
        time.sleep(self.params.get('waiting_time', 0))


        if obs == "Lifetime":
        #to improve accuracy read from "/PETRA/idc/Buffer-0/Current" every second for ~20 seconds 
        #and fit an exp-function to the retrieved data: I(t)=I_0*exp(-t/tau)
        #timerange is a user defined parameter in order to be adjusted
            timerange=self.params.get('timerange', 20)
            data=np.zeros((timerange))
            timestamp=np.zeros((timerange))
            for s in range(timerange):
                data[s], timestamp[s] = self.interface.get_value_with_timestamp("/PETRA/idc/Buffer-0","Current")
                time.sleep(1)
            # Fit the function a * np.exp(b * t) + c to x and y
            tau,_ = curve_fit(lambda t, tau: data[0] * np.exp(-t/tau), np.array(timestamp)-timestamp[0], data)
            return data[0]*tau[0]/3600
        

            
        if obs =="Vertical_Emittance":
            val = self.interface.get_value("PETRA/IfmDiagBeamData/Vertical","Vemittance") 
            return val

        raise NotImplementedError(f"obs {obs} is not implemented.")
    