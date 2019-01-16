from models.units.unit import Unit


class Strategy:
    pass



@Unit.register('army')
class Army(Unit):
    hp = 0
    attack = 0
    strategy_list = {
        0: 'Attack Random',
        1: 'Attack Weakest',
        2: 'Attack Strongest',
    }
    strategy_chosen = None

    def base_hp(self):
        pass

    def cd_update(self):
        pass


    def damage_receive(self, damage):
        pass

    @property
    def damage(self):
        pass

    @property
    def attack_chance(self):
        pass

    def __init__(self, addit_dict=None):
        self._name = addit_dict.pop('name')
        self._strategy = addit_dict.pop('strategy')
        super().__init__(self._name, units=addit_dict)

    def __repr__(self):
        string = 'Brave army num ' + str(self.call_name) + ' consists of:\n'
        for x in self.sub_units:
            string += str(x)
        # string_repr = '\n'.join(list(self.squad_units))
        # print(string_repr)
        # return ''
        return string


