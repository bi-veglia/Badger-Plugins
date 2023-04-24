import pathlib
from badger import interface
import at
     
class Interface(interface.Interface):

    name = 'tine_mock_scan'

    def __init__(self, params=None):
        super().__init__(params)
        path = pathlib.Path(__file__).parent.resolve()
        self.ring = at.load_repr(path / 'lattice' / 'petraIII_lat.repr',energy=6.e9)
        self.indskew = at.get_refpts(self.ring, 'QS[1234]')
        self.ring.radiation_on()

    @staticmethod
    def get_default_params():
        return None

    def get_value(self, channel: str, attr=None):
        print("Called get_value for channel: {}.".format(channel))
        if channel == "PETRA/Cms.MagnetPs/QS1/Strom.Ist":
            I0=at.get_value_refpts(self.ring, self.indskew[0], 'PolynomB', 1)
            return I0[0]
        if channel == 'srdiag/emittance/id07/Emittance_V':
            _, beamdata1, _ = at.ohmi_envelope(self.ring)
            vert_emitt=beamdata1.mode_emittances[1]
            return vert_emitt

    def set_value(self, channel: str, attr: str,value):
        print("Called set_value for channel: {}, with value: {}".format(channel, value))
        if channel == 'PETRA/Cms.MagnetPs/QS1/Strom.Soll':
            at.set_value_refpts(self.ring, self.indskew[0], 'PolynomB', value, 1)
            return
        raise KeyError(f"Channel {channel} is unknown.")