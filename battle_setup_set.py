import json
from random import randint, choice, uniform
from models.units.base_unit import BaseUnit


class ConfigSetup:

    def __init__(self, random=True, armies=None, formations=None, units_per_formation=None):
        self.army_count = randint(2, 3) if random else armies
        self.squads_per_army = randint(2, 5) if random else formations
        self.units_per_squad = randint(2, 5) if random else units_per_formation

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

    def random_unit_config(self, depth=None):
        if depth is None:
            raise AttributeError
        else:
            new_groups = [key for key, group in BaseUnit.GROUPS.items()
                          if group['depth'] > depth]
            random_group = choice(new_groups)
        random_unit = choice(list(BaseUnit.GROUPS[random_group]['units'].keys()))
        return self.default_unit_config(unit_type=random_group, unit_subtype=random_unit)

    def random_squad_config(self):
        depth = BaseUnit.GROUPS['formation']['depth']
        squad_string = {'klass': 'formation', 'type': 'squad',
                        'units': [self.random_unit_config(depth) for _ in range(self.units_per_squad)]}
        return squad_string

    def army_config(self, random=True, strategy=None, army_count=None):
        army_string = dict()
        army_string['klass'] = 'army'
        army_string['type'] = 'squad_army'
        if random:
            army_string['strategy'] = choice(list(BaseUnit.STRATEGIES.keys()))
            army_string['units'] = [self.random_squad_config() for _ in range(self.squads_per_army)]

        return army_string

    def random_battle_config(self):
        battle_setup = {'armies': [self.army_config() for _ in range(self.army_count)]}
        print('created ', self.army_count, ' armies')
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
