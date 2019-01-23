import random
from models.units.unit import Unit


@Unit.register('soldier')
class Soldier(Unit):

    base_hp = 100

    def __init__(self, addit_dict=None):
        if addit_dict is None:
            self._name = "Test George"
        else:
            self._name = addit_dict.pop('name')
        super().__init__(self._name, hp=100)

    def __repr__(self):
        return self.call_name + ' ' + str(self.hp) + 'hp'

    @property
    def is_ready_to_attack(self):
        return self._is_ready_to_attack

    @is_ready_to_attack.setter
    def is_ready_to_attack(self, time):
        self._is_ready_to_attack = True if time - self.last_attack_timestamp >= self._base_cooldown else False
        return

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
