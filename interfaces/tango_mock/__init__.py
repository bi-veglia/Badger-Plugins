import pathlib
import numpy as np
import at
from badger import interface


class Interface(interface.Interface):
    name = 'tango_mock'

    def __init__(self, params=None):
        super().__init__(params)
        path = pathlib.Path(__file__).parent.resolve()
        self.ring = at.load_mat(path / 'model' / 'betamodel.mat', mat_key='betamodel')
        self.indskew = at.get_refpts(self.ring, 'S[HFDIJ]*')
        self.ring.radiation_on()
        self.skewnames=[]
        for i in self.ring[self.indskew]:
            self.skewnames.append(i.FamName)
        self.sf2a=np.zeros((288))
        for j in range(len(self.indskew)):
            if self.skewnames[j].startswith('SF2A'):
                self.sf2a[j]=1
        sf2a_ind=np.where(self.sf2a>0)
        for i in range(len(self.sf2a)):
            if i==sf2a_ind[0][3]:
                self.sf2a[i]=1
            else:
                self.sf2a[i]=0
        np.random.seed(22)
        #self.sqpinput = 0.01*np.random.rand((288))
        self.sqpinput = 0.1*np.random.rand((len(self.indskew)))*self.sf2a

    @staticmethod
    def get_default_params():
        return None

    def get_value(self, channel: str, attr=None):
        print('Called get_value for channel: {}.'.format(channel))
        if channel == 'srdiag/emittance/id07/Emittance_V':
            _, beamdata1, _ = at.ohmi_envelope(self.ring)
            vert_emitt=beamdata1.mode_emittances[1]
            return vert_emitt

        raise KeyError(f"Channel {channel} is unknown.")

    def set_value(self, channel: str, attr: str, value):
        print("Called set_value for channel: {}, with value: {}".format(channel, value))
        if channel == 'srmag/sqp/all':
            print(f"value: {type(value)}")
            print(f"sqpinput: {type(self.sqpinput)}")
            #at.set_value_refpts(self.ring, self.indskew, 'PolynomA', value + self.sqpinput, 1)
            return
        if channel == 'srmag/sqp/SF2A':
            print(f"value: {type(value)}")
            print(f"sqpinput: {type(self.sqpinput)}")
            at.set_value_refpts(self.ring, self.indskew, 'PolynomA', value + self.sqpinput, 1)
            return
        raise KeyError(f"Channel {channel} is unknown.")
    