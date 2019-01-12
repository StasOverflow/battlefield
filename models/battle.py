from models.units.unit import Unit
from models.units.army.army import Army
from models.units.soldier.soldier import Soldier
from models.units.vehicle.vehicle import Vehicle
from models.units.squad.squad import Squad
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
        print("Preparing armies")
        self._participants = list()
        if incoming_config is None:
            raise Exception('No incoming config file')
        else:
            with open(incoming_config) as conf:
                data = json.load(conf)
                main_key = list(data.keys())[0]
                for units in data[main_key]:
                    self._participants.append(Unit.new(units.pop('type'), units))

    def setup_set(self, setup):
        data = json.load(setup)
        print(data)

    def setup_create(self, randomly=0):
        print("Da")
