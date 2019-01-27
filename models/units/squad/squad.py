from models.units.unit import Unit


@Unit.register('squad')
class Squad(Unit):
    hp = 0
    attack = 0
    damage = 0

    @property
    def attack_damage(self):
        pass

    def damage_receive(self, damage):
        pass

    @property
    def is_ready_to_attack(self):
        pass

    @is_ready_to_attack.setter
    def is_ready_to_attack(self, time):
        pass

    @property
    def attack_chance(self):
        pass

    def __init__(self, addit_dict=None):
        self.call_name = addit_dict.pop('name')
        super().__init__(self.call_name, units=addit_dict)

    def __repr__(self):
        string = '\n--------------\nsquad' + ' num ' + self.call_name + ':\n'
        for unit in self.sub_units:
            string = string + '\n' + str(unit)
        string = string + '\n--------------\n'
        return string

    @property
    def is_alive(self):
        pass
