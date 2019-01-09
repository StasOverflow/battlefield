import json

from models.units import *
# from models.units import unit
# import models.units as units

import random

from models.units.unit import Unit


def random_config_create():
    army_count = random.randint(2, 5)
    squads_per_army = random.randint(4, 15)
    units_per_squad = random.randint(5, 12)

    def default_unit_config(unit_type):
        some_unit_stats = {'type': unit_type}
        if unit_type == 'soldier':
            some_unit_stats['hp'] = Unit.UNIT[unit_type].base_hp()
        else:
            some_unit_stats['operators'] = [default_unit_config('soldier') for _ in range(3)]
        return some_unit_stats

    def random_string_unit():
        return default_unit_config(random.choice(list(Unit.UNIT.keys())))

    def random_squad_config(squad_name):
        squad_string = {'name': squad_name, 'units': [random_string_unit() for _ in range(units_per_squad)]}
        return squad_string

    def random_army_config(army_name):
        army_string = {'name': army_name, 'strategy': random.randint(0, 2)}
        squad_name = str(army_name) + '.'
        army_string['squads'] = [random_squad_config(squad_name + str(x+1)) for x in range(squads_per_army)]
        return army_string

    battle_setup = {'armies': [random_army_config(x) for x in range(army_count)]}

    with open('battle_config.json', 'w') as outfile:
        json.dump(battle_setup, outfile, indent=4)


if __name__ == '__main__':
    random_config_create()
