from models.units.unit import Unit


class Strategy:
    pass



@Unit.register('army')
class Army(Unit):
    hp = 0
    attack = 0
    squad_units = list()
    strategy_list = {
        0: 'Attack Random',
        1: 'Attack Weakest',
        2: 'Attack Strongest',
    }
    strategy_chosen = None

    def __init__(self, addit_dict=None):
        self._name = addit_dict.pop('name')
        self._strategy = addit_dict.pop('strategy')
        super().__init__(self._name, hp=100)
        main_key = list(addit_dict.keys())[0]
        print(main_key)
        for units in addit_dict[main_key]:
            self.squad_units.append(Unit.new(units.pop('type'), units))

    def __repr__(self):
        for x in self.squads:
            print(x)
        # string_repr = '\n'.join(self.squads)
        return ''



