import time
import numpy as np
from badger import environment
from badger.interface import Interface


class Environment(environment.Environment):

    name = 'petraIII'

    def __init__(self, interface: Interface, params):
        super().__init__(interface, params)
        self.channel_to_tine_params = {var: (var.split('/')[:-1], var.split('/')[-1]) for var in self.list_vars()}

    def _get_vrange(self, var):
        return {"PETRA/Cms.MagnetPs/QS1/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS2/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS3/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS4/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_W1/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_W2/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_W3/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_W4/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_N1/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_N2/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_N3/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_N4/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_NO1/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_O3/Strom.Soll": [-0.5, 0.5],
                "PETRA/Cms.MagnetPs/QS_O4/Strom.Soll": [-0.5, 0.5], }[var]

    @staticmethod
    def list_vars():
        return ["PETRA/Cms.MagnetPs/QS1/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS2/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS3/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS4/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_W1/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_W2/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_W3/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_W4/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_N1/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_N2/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_N3/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_N4/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_NO1/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_O3/Strom.Soll",
                "PETRA/Cms.MagnetPs/QS_O4/Strom.Soll",]

    @staticmethod
    def list_obses():
        return ['PETRA/DiagBeamData/Direkt/VEmittance',
                "PETRA/IfmDiagBeamData/Vertical/VEmittance"]

    @staticmethod
    def get_default_params():
        return {
            'waiting_time': 1,
        }

    def _get_var(self, var):
        tine_channel, prop = self.channel_to_tine_params[var]
        return self.interface.get_value(tine_channel, prop)

    def _set_var(self, var, x):
        tine_channel, prop = self.channel_to_tine_params[var]
        self.interface.set_value(tine_channel, prop, x)

    def _get_obs(self, obs):
        time.sleep(self.params.get('waiting_time', 0))

        if obs == "PETRA/DiagBeamData/Direkt/VEmittance":
            tine_channel, prop = self.channel_to_tine_params[obs]
            return self.interface.get_value(tine_channel, prop)
        elif obs == "PETRA/IfmDiagBeamData/Vertical/VEmittance":
            tine_channel, prop = self.channel_to_tine_params[obs]
            return self.interface.get_value(tine_channel, prop)

        raise NotImplementedError(f"obs {obs} is not implemented.")
