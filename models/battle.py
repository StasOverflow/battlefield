from models.units.base_unit import Unit
import json
import time
import math


class BattleTimer:

    def __init__(self, multiplier, battle_timer_getter_func=time.monotonic):
        print(battle_timer_getter_func)
        self._start_time = battle_timer_getter_func()
        self._timer_func = battle_timer_getter_func
        self._timer_multiplier = multiplier

    @property
    def time(self):
        return round((self._timer_func() - self._start_time)*self._timer_multiplier, 3)


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
        self._participants = list()
        if incoming_config is None:
            raise Exception('No incoming config file')
        else:
            with open(incoming_config) as conf:
                army_count = 0
                data = json.load(conf)
                main_key = list(data.keys())[0]
                for units in data[main_key]:
                    self._participants.append(Unit.new(units.pop('type'), units))
                    army_count = len(data[main_key])
                print("initiating battle with", army_count, 'armies')
        for army in self._participants:
            print(army)

    def setup_set(self, setup):
        data = json.load(setup)
        print(data)

    def setup_create(self, randomly=0):
        print("Da")
