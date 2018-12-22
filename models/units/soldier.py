from .unit import Unit


class Soldier(Unit):

    def __init__(self):
        self.attack_success_prob = 3
        self.hp = 100
        self.recharge_time = 1

    def hp_get(self):
        return self.hp

    def successful_attack_chance(self):
        return True

    def damage_deal(self):
        return self.damage

    def damage_receive(self):
        self.hp = self.hp - 100