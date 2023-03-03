import PyTine as pt
from badger import interface


class Interface(interface.Interface):

    name = 'tine'

    def __init__(self, params=None):
        super().__init__(params)

    @staticmethod
    def get_default_params():
        return None

    def get_value(self, channel: str, property: str):
        val = pt.get(channel, property)
        return val['data']

    def set_value(self, channel: str, property: str, value):
        pt.set(channel, property, input=value)
