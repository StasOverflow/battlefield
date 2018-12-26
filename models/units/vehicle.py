from .unit import Unit
from .soldier import Soldier


@Unit.register('vehicle')
class Vehicle(Unit):
    operators = []
    vehicle_hp = 0

    def __init__(self):
        print('ima vehicle')
        self.attack_success_prob = 3
        self.recharge_time = 5
        self.operators = [Soldier() for _ in range(3)]
        self.vehicle_hp = 500
        self.hp = self.hp_get()

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
        