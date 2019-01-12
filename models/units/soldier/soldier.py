import random
from models.units.unit import Unit


@Unit.register('soldier')
class Soldier(Unit):

    _base_hp = 100
    recharge_time = 200

    @property
    def is_alive(self):
        return True if self._hp > 0 else False

    @property
    def base_recharge_time(self):
        return self.recharge_time

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    def __init__(self, addit_dict=None):
        self._name = addit_dict.pop('name')
        super().__init__(self._name, hp=100)

    def random_value(self):
        value = random.randint(1, 6)
        if value > 3:
            print('x')
        else:
            print('y')

    def hp_get(self):
        return self.hp

    def successful_attack_chance(self):
        return True

    def damage_deal(self):
        return self.damage

    def damage_receive(self):
        self.hp = self.hp - 100
