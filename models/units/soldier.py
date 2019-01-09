from .unit import Unit


@Unit.register('soldier')
class Soldier(Unit):

    _base_hp = 100
    recharge_time = 200

    @property
    def base_recharge_time(self):
        return self.recharge_time

    @property
    def health(self):
        pass

    @health.setter
    def health(self):
        pass

    def __init__(self):
        super().__init__(BASE_HP, BASE_RECHARGE_TIME)
        print('ima soldier')
        self._xp = 0

    def hp_get(self):
        return self.hp

    def successful_attack_chance(self):
        return True

    def damage_deal(self):
        return self.damage

    def damage_receive(self):
        self.hp = self.hp - 100
