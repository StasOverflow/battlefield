from models.units.base_unit import BaseUnit
import json
import time


def get_unit_from_json(json_file):
    if json_file is None:
        raise Exception('Missing config file for soldier!')
    else:
        with open(json_file) as conf:
            data = json.load(conf)
            # print(data)
            # type_of = data.pop('type')
            unit_instance = BaseUnit.new(**data)
    return unit_instance


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

        vehicle_1 = get_unit_from_json('tests/test_vehicle.json')
        vehicle_2 = get_unit_from_json('tests/test_vehicle.json')

        soldja_uno = get_unit_from_json('tests/test_soldier.json')
        soldja_two = get_unit_from_json('tests/test_soldier.json')

        unit1 = vehicle_1
        unit2 = vehicle_2

        for i in range(5000000):
            if self.vice_versa:
                attack = unit1.engage(unit2)
            else:
                attack = unit2.engage(unit1)
            self.vice_versa = not self.vice_versa
            if attack:
                print('round result: \n', str(unit1), '\n', str(unit2), '\n', '_'*80)

    # def battle_vehicles(self):

    def setup_set(self, setup):
        data = json.load(setup)
        print(data)

    def setup_create(self, randomly=0):
        print("Da")
