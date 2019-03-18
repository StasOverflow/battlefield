from models.units.base_unit import Unit


@Unit.register('squad')
class Squad(Unit):

    def __init__(self, addit_dict=None):
        if addit_dict is None:
            initial_call_name = "Test Squad"
        else:
            initial_call_name = addit_dict.pop('name')
        super().__init__(call_name=initial_call_name, units=addit_dict)

    def __repr__(self):
        string = '\n--------------\nsquad'  \
                 + ' num '                  \
                 + self.call_name           \
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
