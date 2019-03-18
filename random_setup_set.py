import json
from random import randint, choice
from models.units.base_unit import BaseUnit


def random_config_create():
    army_count = randint(2, 5)
    squads_per_army = randint(4, 15)
    units_per_squad = randint(5, 12)

    def default_unit_config(unit_type):
        some_unit_stats = {'type': unit_type, 'hp': BaseUnit.UNIT[unit_type].base_hp}
        if unit_type == 'dpv':
            some_unit_stats['cd'] = randint(1001, 2000)
            some_unit_stats['operators'] = [default_unit_config('soldier') for _ in range(3)]
        elif unit_type == 'soldier':
            some_unit_stats['cd'] = randint(100, 1000)
        return some_unit_stats

    def random_string_unit():
        return default_unit_config(choice(list(BaseUnit.UNIT.keys())))

    def random_squad_config():
        squad_string = {'type': 'squad',
                        'units': [random_string_unit() for _ in range(units_per_squad)]}
        return squad_string

    def random_army_config():
        army_string = dict()
        army_string['type'] = 'army'
        army_string['strategy'] = randint(0, 2)
        army_string['squads'] = [random_squad_config() for _ in range(squads_per_army)]
        return army_string

    battle_setup = {'armies': [random_army_config() for _ in range(army_count)]}

    with open('combat_setup.json', 'w') as outfile:
        json.dump(battle_setup, outfile, indent=4)


if __name__ == '__main__':
    random_config_create()
