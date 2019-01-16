import random
from models.units.unit import Unit


@Unit.register('soldier')
class Soldier(Unit):

    _base_hp = 100
    recharge_time = 200

    def __init__(self, addit_dict=None):
        self._name = addit_dict.pop('name')
        super().__init__(self._name, hp=100)

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, success):
        if success:
            self.experience += 1

    def damage_receive(self, damage):
        pass

    @property
    def damage(self):
        pass

    @property
    def attack_chance(self):
        pass

    @property
    def base_recharge_time(self):
        return self.recharge_time

    def random_value(self):
        value = random.randint(1, 6)
        if value > 3:
            print('x')
        else:
            print('y')

    def __repr__(self):
        return self.call_name + ' ' + str(self.hp) + 'hp'
