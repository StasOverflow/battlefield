from models.units.base_unit import BaseUnit


# @BaseUnit.register('squad')
class Squad(BaseUnit):

    def __init__(self, addit_dict=None):
        super().__init__(units=addit_dict)

    def __repr__(self):
        string = '\n--------------\nsquad'  \
                 + ' num '                  \
                 + ':\n'
        for unit in self.sub_units:
            string = string + '\n' + str(unit)
        string = string + '\n--------------\n'
        return string

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
