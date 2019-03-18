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

    # def engage(self, attacking_unit, defending_unit):
    #     """
    #     Performs the following:
    #         -calculates successful attack probability form each of battling sides
    #         -sets 'prepared' property of attacking unit to False, allowing to recalculate
    #          attack chance on the next engagement
    #         -performs an attack if attacking side unit's attack chance is more than
    #          defending side unit's one (by triggering attack_won|lost methods)
    #         -starts cooldown for attacking unit
    #
    #     :param attacking_unit:
    #     :param defending_unit:
    #     :return: True if attack performed, False otherwise
    #     """
    #     if attacking_unit.ready_to_attack():
    #         attacking_unit.attack_chance_calculate()
    #         attacking_unit.is_prepared = False
    #         atk_side_chance = attacking_unit.attack_chance
    #         def_side_chance = defending_unit.attack_chance
    #         if atk_side_chance > def_side_chance:
    #             attacking_unit.attack_won()
    #             defending_unit.attack_lost(attacking_unit.attack_damage)
    #         attacking_unit.reload()
    #         return True
    #     else:
    #         return False

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

        for i in range(5000000):
            if self.vice_versa:
                attack = soldja_uno.engage(soldja_two)
            else:
                attack = soldja_two.engage(soldja_uno)
            self.vice_versa = not self.vice_versa
            if attack:
                print('round result: \n', str(soldja_uno), '\n', str(soldja_two), '\n', '_'*80)
        # if incoming_config is None:
        #     raise Exception('No incoming config file')
        # else:
        #     with open(incoming_config) as conf:
        #         army_count = 0
        #         data = json.load(conf)
        #         main_key = list(data.keys())[0]
        #         for units in data[main_key]:
        #             self._participants.append(Unit.new(units.pop('type'), units))
        #             army_count = len(data[main_key])
        #         print("initiating battle with", army_count, 'armies')
        # for army in self._participants:
        #     print(army)

    def setup_set(self, setup):
        data = json.load(setup)
        print(data)

    def setup_create(self, randomly=0):
        print("Da")
