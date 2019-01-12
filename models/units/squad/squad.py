from models.units.unit import Unit


@Unit.register('squad')
class Squad(Unit):
    hp = 0
    attack = 0
    damage = 0
    call_sign = ''
    battle_units = list()

    def __init__(self, addit_dict=None):
        self._name = addit_dict.pop('name')
        super().__init__(self._name, hp=100)
        main_key = list(addit_dict.keys())[0]
        print(main_key)
        for units in addit_dict[main_key]:
            self.battle_units.append(Unit.new(units.pop('type'), units))



    def __repr__(self):
        print("i have this many units ", len(self.units))
        string = self.call_sign
        print(string)
        for x in self.units:
            print(x)
        # string = string + '\n'.join(str(self.units))
        return ''
