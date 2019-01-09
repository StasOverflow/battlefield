from models.units.unit import Unit
import models.units.soldier
import models.units.vehicle


class Army:
    hp = 0
    attack = 0
    squads = []
    strategy_list = {
        0: 'Attack Random',
        1: 'Attack Weakest',
        2: 'Attack Strongest',
    }
    strategy_chosen = None

    def __init__(self, strategy_type, squad_quantity, units_per_squad):
        self.strategy_chosen = self.strategy_list[strategy_type]
        self.squads = [Squad(units_per_squad, x) for x in range(squad_quantity)]

    def __repr__(self):
        for x in self.squads:
            print(x)
        # string_repr = '\n'.join(self.squads)
        return ''


class Squad:
    hp = 0
    attack = 0
    damage = 0
    call_sign = ''

    def __init__(self, unit_quantity, call):
        unit_types = list(Unit.UNIT)
        print(unit_types)
        self.units = [Unit.new() for _ in range(unit_quantity)]

    def __repr__(self):
        print("i have this many units ", len(self.units))
        string = self.call_sign
        print(string)
        for x in self.units:
            print(x)
        # string = string + '\n'.join(str(self.units))
        return ''



