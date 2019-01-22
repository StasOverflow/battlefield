from models.units.unit import Unit
from models.units.soldier.soldier import Soldier


@Unit.register('vehicle')
class Vehicle(Unit):
    vehicle_hp = 0

    _base_hp = 200
    recharge_time = 200

    def cd_update(self):
        pass

    @property
    def is_ready_to_attack(self):
        return self._is_ready_to_attack

    @is_ready_to_attack.setter
    def is_ready_to_attack(self, time):
        self._is_ready_to_attack = True if time - self.last_attack_timestamp >= self._base_cooldown else False
        return

    def damage_receive(self, damage):
        pass

    @property
    def damage(self):
        pass

    @property
    def attack_chance(self):
        pass

    @property
    def base_health(self):
        return self._base_hp

    @property
    def base_recharge_time(self):
        return self.recharge_time

    def __init__(self, addit_dict=None):
        self._name = addit_dict.pop('name')
        hp = addit_dict.pop('hp')
        super().__init__(self._name, hp=self._base_hp)

    def hp_get(self):
        hp = 0
        for soldier in self.sub_units:
            hp = hp + soldier.hp_get()
        hp = hp + self.vehicle_hp
        return hp

    def successful_attack_chance(self):
        return True

    def damage_deal(self):
        return self.damage

    def damage_receive(self):
        self.hp = self.hp - 100

    def __repr__(self):
        return self.call_name + ' ' + str(self.hp) + 'hp'
