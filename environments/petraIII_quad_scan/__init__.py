import time
import numpy as np
from scipy.optimize import curve_fit
from badger import environment
from badger.interface import Interface



class Environment(environment.Environment):

    name = 'petraIII_quad_scan'

    def __init__(self, interface: Interface, params):
        self.current_vars = []
        super().__init__(interface, params)
        # mapping from badger addresses to tine addresses 
        #self.channel_to_tine_params = {var: ("/".join(var.split('/')[:-1]), var.split('/')[-1]) for var in self.list_vars() + self.list_obses()}                                     
        #self.init_values = {channel : self._get_var(channel) for channel in self.list_vars()}

    
    @staticmethod
    def list_vars():
        return ["PETRA/Cms.MagnetPs/QS1/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS1/Strom.Ist"]

    @staticmethod
    def list_obses():
        return ['Lifetime','Vertical_Emittance']
    

    @staticmethod
    def get_default_params():
        return {
            'waiting_time': 1,
            'timerange': 20,
        }

    def _get_var(self, vars):
        print(f"requested values: {vars}")
        self.current_vars=self.interface.get_value(channel='PETRA/Cms.MagnetPs/QS1/Strom.Ist')    
        return self.current_vars

    def _set_var(self, vars, _x):
        self.current_vars = _x
        self.interface.set_value(channel='PETRA/Cms.MagnetPs/QS1/Strom.Soll', attr='PolynomB', value=_x) 

    def _get_obs(self, obs):
        print("Calling _get_obs")
        time.sleep(self.params.get('waiting_time', 1))     
    
        if obs =="Vertical_Emittance":
            val = self.interface.get_value("srdiag/emittance/id07/Emittance_V","Vemittance") 
            return val

        raise NotImplementedError(f"obs {obs} is not implemented.")
