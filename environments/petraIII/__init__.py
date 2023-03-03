import time
import numpy as np
from badger import environment
from badger.interface import Interface



class Environment(environment.Environment):

    name = 'petraIII'

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.channel_to_tine_params = {var: ("/".join(var.split('/')[:-1]), var.split('/')[-1]) for var in self.list_vars() + self.list_obses()}

    def _get_vrange(self, var):
        return {"PETRA/Cms.MagnetPs/QS1/Strom.Soll": [-5., 5.],
                "PETRA/Cms.MagnetPs/QS2/Strom.Soll": [-5., 5.],
                "PETRA/Cms.MagnetPs/QS3/Strom.Soll": [-5., 5.],
                "PETRA/Cms.MagnetPs/QS4/Strom.Soll": [-5., 5.], }[var]

    @staticmethod
    def list_vars():
        return ["PETRA/Cms.MagnetPs/QS1/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS2/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS3/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS4/Strom.Soll",]

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
        print(f"tine_channel: {tine_channel}")
        print(f"prop: {prop}")
        return self.interface.get_value(tine_channel, prop)

    def _set_var(self, var, x):
        tine_channel, prop = self.channel_to_tine_params[var]
        self.interface.set_value(tine_channel, prop, x)

    def _get_obs(self, obs):
        time.sleep(self.params.get('waiting_time', 0))


        if obs == "PETRA/Lifetime/#0/Tau":
            tine_channel, prop = self.channel_to_tine_params[obs]
            val = self.interface.get_value(tine_channel, prop) # returns a list with three elements (e.g [8.410006523132324, 8.410006523132324, 15.865203857421875])
            return val[2]

        raise NotImplementedError(f"obs {obs} is not implemented.")
    
if __name__ == "__main__":
    import sys
    sys.path.insert(1, '/Users/pecon/projects/bianca/Badger-Plugins/interfaces')
    from tine import Interface

    print("Start Test...")
    petra = Environment(Interface(), None)
    var_qs1 = petra._get_var("PETRA/Cms.MagnetPs/QS1/Strom.Soll")
    print(f"PETRA/Cms.MagnetPs/QS1/Strom.Soll : {var_qs1}")

    var_tau = petra._get_obs("PETRA/Lifetime/#0/Tau")
    print(f"PETRA/Lifetime/#0/Tau : {var_tau}")