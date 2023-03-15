from numpy import random
from badger import interface


class Interface(interface.Interface):

    name = 'tine_mock'

    def __init__(self, params=None):
        super().__init__(params)

    @staticmethod
    def get_default_params():
        return None

    def get_value(self, channel: str, property: str):
        print("Called get_value for channel: {}.".format(channel))
        return random.random()

    def set_value(self, channel: str, property: str, value):
        print(f"channel {channel}, property: {property}, value: {value}")

