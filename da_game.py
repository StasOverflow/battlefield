import random


class Army:
    hp = 0
    attack = 0
    squads = []
    strategy_list = {
        0: 'Attack Random',
        1: 'Attack Weakest',
        2: 'Attack Strongest',
    }
    strategy_chosen = None

    def __init__(self, strategy_type, squad_quantity, units_per_squad):
        self.strategy_chosen = self.strategy_list[strategy_type]
        self.squads = [Squad(units_per_squad) for _ in range(squad_quantity)]

    def __repr__(self):
        string_repr = ''
        # for squad in self.squads:
        #     for unit in squad:
        #         if type(unit) is Vehicle:
        #             string_repr = string_repr +


class Squad:
    hp = 0
    attack = 0
    damage = 0
    units = []

    def __init__(self, unit_quantity):
        for i in range(unit_quantity):
            seed = random.randint(0, 5)
            if not seed:
                unit = Vehicle()
            else:
                unit = Soldier()
            self.units.append(unit)
            print(unit)


class Unit:
    hp = 0
    recharge_time = 0
    damage = 0
    attack_success_prob = 0
    damage = 0
    cooldown = 0

    def __repr__(self):
        type_of = self.__class__.__name__

        # type_of = type_of.split()
        print(type_of)
        repr_string = '|HP: ' + str(self.hp) + '|DMG :' + str(self.damage) + '|cd ' + str(self.cooldown) + '|'
        print(repr_string)
        return repr_string


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


class Vehicle(Unit):
    operators = []
    vehicle_hp = 0

    def __init__(self):
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


