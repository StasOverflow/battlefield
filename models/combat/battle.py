from models.units.base_unit import BaseUnit
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

        self.vice_versa = False
        # print(BaseUnit.GROUPS)
        soldja_uno = BaseUnit.new('soldier')
        soldja_two = BaseUnit.new('soldier')

        # vehicle_1 = BaseUnit.new('dpv')
        # vehicle_2 = BaseUnit.new('dpv')

        for i in range(5000000):
            if self.vice_versa:
                attack = soldja_uno.engage(soldja_two)
            else:
                attack = soldja_two.engage(soldja_uno)
            self.vice_versa = not self.vice_versa
            if attack:
                print('round result: \n', str(soldja_uno), '\n', str(soldja_two), '\n', '_'*80)

    def setup_set(self, setup):
        data = json.load(setup)
        print(data)

    def setup_create(self, randomly=0):
        print("Da")
