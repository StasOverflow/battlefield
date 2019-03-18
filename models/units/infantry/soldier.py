import random
from models.units.base_unit import Unit


@Unit.register('soldier')
class Soldier(Unit):

    base_hp = 100
    base_recharge_time = 200

    def __init__(self, addit_dict=None):
        self.hp = 0
        if addit_dict is None:
            initial_call_name = "Test George"
            initial_hp = self.base_hp
            initial_cd = self.base_recharge_time
        else:
            initial_call_name = addit_dict.pop('name')
            initial_hp = addit_dict.pop('hp')
            initial_cd = addit_dict.pop('cd')
        self._experience = 0
        super().__init__(call_name=initial_call_name, hp=initial_hp, cooldown=initial_cd)

    def __repr__(self):
        return self.call_name + ' ' + str(self.hp) + 'hp'

    @property
    def attack_damage(self):
        attack_damage = 0
        if self.is_alive:
            attack_damage = 0.05 + self.experience / 100
        return attack_damage

    def damage_receive(self, damage):
        self.hp = self.hp - damage

    @property
    def attack_chance(self):
        return 0.5 * (1 + self.hp/100) * random.randint(50 + self.experience, 100) / 100

    def is_ready_to_attack_at_the_moment(self, time):
        return True if time - self.last_attack_timestamp >= self.recharge_time else False

    @property
    def experience(self):
        if self.is_alive:
            experience = self._experience
        else:
            experience = 0
        return experience

    @experience.setter
    def experience(self, exp_value):
        if self._experience is 0:
            self._experience = exp_value
        else:
            self._experience = self._experience + exp_value
        if self.experience >= 50:
            self._experience = 50
        elif self.experience <= 0:
            self._experience = 0
        return

    def experience_receive(self, success):
        if success:
            self.experience += 1

    @property
    def hp(self):
        return super().hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if self.hp < 0:
            self._hp = 0
        return

    @property
    def is_alive(self):
        return True if self.hp > 0 else False

    def random_value(self):
        value = random.randint(1, 6)
        if value > 3:
            print('x')
        else:
            print('y')
