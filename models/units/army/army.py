from models.units.unit import Unit


@Unit.register('army')
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

    def __init__(self, name, strategy, **kwargs):
        self._name = name
        self._strategy = strategy
        print(kwargs)
        # self.strategy_chosen = self.strategy_list[strategy_type]
        # self.squads = [Squad(units_per_squad, x) for x in range(squad_quantity)]

    def __repr__(self):
        for x in self.squads:
            print(x)
        # string_repr = '\n'.join(self.squads)
        return ''



