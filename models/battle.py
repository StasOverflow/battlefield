from .army import Army
import json


class Battle:
    setup = {}
    army_count = 0
    squads_per_army_count = 0
    units_per_squad_count = 0

    def incoming_config_parse(self, config):
        self.army_count = 2
        self.squads_per_army_count = 4
        self.units_per_squad_count = 1

    def __init__(self, incoming_config=None):
        if incoming_config is None:
            raise Exception('No incoming config file')
        else:
            with open(incoming_config) as conf:
                data = json.load(conf)
                print(data)

    def setup_set(self, setup):
        data = json.load(setup)
        print(data)

    def setup_create(self, randomly=0):
        print("Da")
