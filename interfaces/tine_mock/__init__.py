from numpy import random
from badger import interface
import time

saved_values = {}
foobar = None

class Interface(interface.Interface):

    name = 'tine_mock'

    def __init__(self, params=None):
        super().__init__(params)

    @staticmethod
    def get_default_params():
        return None

    def get_value(self, channel: str, property: str):
        print("Called get_value for channel: {}.".format(channel))
        if not (channel + property) in saved_values:
            saved_values[channel + property] = random.random()
        if channel == "PETRA/idc/Buffer-0" and foobar is not None:
            return foobar
        return saved_values[channel + property]
    
    def get_value_with_timestamp(self, channel: str, property: str):
        # int(time.time())
        return self.get_value(channel, property), int(time.time())

    def set_value(self, channel: str, property: str, value):
        print(f"channel {channel}, property: {property}, value: {value}")
        global foobar
        foobar = value
        saved_values[channel + property] = value

