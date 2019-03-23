import json
from random import randint, choice, uniform
from models.units.base_unit import BaseUnit


class ConfigSetup:

    def __init__(self, random=True, armies=None, formations=None, units_per_formation=None):
        self.army_count = randint(2, 5) if random else armies
        self.squads_per_army = randint(4, 15) if random else formations
        self.units_per_squad = randint(5, 12) if random else units_per_formation

    def randomize_value(self, value):
        """
        Used to get randomish new value, from a given, by selecting a random point
        between 50% and 150% of a given value
        """
        if value is not None:
            btm_border = value * 0.5
            top_border = value * 1.5
            return float("{0:.3f}".format(uniform(btm_border, top_border)))
        else:
            return None

    def default_unit_config(self, unit_type, unit_subtype):
        unit = BaseUnit.GROUPS[unit_type]['units'][unit_subtype]
        some_unit_stats = {'klass': unit_type, 'type': unit_subtype,
                           'hp': unit.base_hp, 'cd': self.randomize_value(unit.base_recharge_time)}
        if unit_type == 'vehicle':
            some_unit_stats['units'] = [self.default_unit_config(unit_type='infantry',
                                                                 unit_subtype='soldier') for _ in range(3)]
        return some_unit_stats

    def random_unit_config(self):
        random_group = choice(list(BaseUnit.GROUPS.keys()))
        random_unit = choice(list(BaseUnit.GROUPS[random_group]['units'].keys()))
        return self.default_unit_config(unit_type=random_group, unit_subtype=random_unit)

    def random_squad_config(self):
        squad_string = {'type': 'squad',
                        'units': [self.random_unit_config() for _ in range(self.units_per_squad)]}
        return squad_string

    def random_army_config(self):
        army_string = dict()
        army_string['type'] = 'army'
        army_string['strategy'] = randint(0, 2)
        army_string['squads'] = [self.random_squad_config() for _ in range(self.squads_per_army)]
        return army_string

    def random_battle_config(self):
        battle_setup = {'armies': [self.random_army_config() for _ in range(self.army_count)]}
        return battle_setup

    def setup_create(self, setup=None, to_json=True, path_to_output_file='combat_setup.json'):
        with open(path_to_output_file, 'w') as outfile:
            data = json.dumps(setup, indent=4)
            json.dump(setup, outfile, indent=4)
        return data


if __name__ == '__main__':
    configurator = ConfigSetup()
    setup = configurator.random_battle_config()
    configurator.setup_create(setup=setup)
