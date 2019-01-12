from models.units.unit import Unit
from models.units.soldier.soldier import Soldier


@Unit.register('vehicle')
class Vehicle(Unit):
    operators = []
    vehicle_hp = 0

    _base_hp = 200
    recharge_time = 200

    @property
    def base_health(self):
        return self._base_hp

    @property
    def base_recharge_time(self):
        return self.recharge_time

    def __init__(self, addit_dict=None):
        self._name = addit_dict.pop('name')
        hp = addit_dict.pop('hp')
        super().__init__(self._name, hp=100)
        main_key = list(addit_dict.keys())[0]
        print("main key is", main_key)
        for units in addit_dict[main_key]:
            self.operators.append(Unit.new(units.pop('type'), units))

    def hp_get(self):
        hp = 0
        for soldier in self.operators:
            hp = hp + soldier.hp_get()
        hp = hp + self.vehicle_hp
        return hp

    def successful_attack_chance(self):
        return True

    def damage_deal(self):
        return self.damage

    def damage_receive(self):
        self.hp = self.hp - 100

