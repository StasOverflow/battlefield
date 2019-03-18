import json
from random import randint, choice
from models.units.base_unit import Unit
from models.units.vehicles.desert_patrol_vehicle import DPV
from models.units.infantry.soldier import Soldier


def _workaround():
    """
    Prevents pycharm from deleting imports on refactor
    (silly as it is)
    """
    DPV()
    Soldier()
    return None


def random_config_create():
    army_count = randint(2, 5)
    squads_per_army = randint(4, 15)
    units_per_squad = randint(5, 12)

    def default_unit_config(unit_type):
        some_unit_stats = {'type': unit_type, 'hp': Unit.UNIT[unit_type].base_hp}
        if unit_type == 'dpv':
            some_unit_stats['cd'] = randint(1001, 2000)
            some_unit_stats['name'] = 'Pepelats'
            some_unit_stats['operators'] = [default_unit_config('soldier') for _ in range(3)]
        elif unit_type == 'soldier':
            some_unit_stats['cd'] = randint(100, 1000)
            some_unit_stats['name'] = 'Steve'
        return some_unit_stats

    def random_string_unit():
        return default_unit_config(choice(list(Unit.UNIT.keys())))

    def random_squad_config(squad_name):
        squad_string = {'type': 'squad', 'name': squad_name, 'units': [random_string_unit() for _ in range(units_per_squad)]}
        return squad_string

    def random_army_config(army_name):
        army_string = {'type': 'army', 'name': army_name, 'strategy': randint(0, 2)}
        squad_name = str(army_name) + '.'
        army_string['squads'] = [random_squad_config(squad_name + str(x+1)) for x in range(squads_per_army)]
        return army_string

    battle_setup = {'armies': [random_army_config(x) for x in range(army_count)]}

    with open('battle_config.json', 'w') as outfile:
        json.dump(battle_setup, outfile, indent=4)


if __name__ == '__main__':
    random_config_create()
