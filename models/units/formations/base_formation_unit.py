from models.units.base_unit import BaseUnit

#
# @BaseUnit.register_group('formations', 'squad, 7000)
# class Squad(BaseUnit):
#
#     def __init__(self, addit_dict=None):
#         super().__init__(units=addit_dict)
#
#     def __repr__(self):
#         string = '\n--------------\nsquad'  \
#                  + ' num '                  \
#                  + ':\n'
#         for unit in self.sub_units:
#             string = string + '\n' + str(unit)
#         string = string + '\n--------------\n'
#         return string
#
#     @property
#     def attack_damage(self):
#         attack_damage = 0
#         if self.is_alive:
#             attack_damage = 0.05 + self.experience / 100
#         return attack_damage
#
#     def damage_receive(self, damage):
#         self.hp = self.hp - damage
#
#     @property
#     def attack_chance(self):
#         return 0.5 * (1 + self.hp/100) * random.randint(50 + self.experience, 100) / 100
#
#     def is_ready_to_attack_at_the_moment(self, time):
#         return True if time - self.last_attack_timestamp >= self.recharge_time else False
#
#     @property
#     def hp(self):
#         return super().hp
#
#     @hp.setter
#     def hp(self, value):
#         self._hp = value
#         if self.hp < 0:
#             self._hp = 0
#         return
#
#     @property
#     def is_alive(self):
#         return True if self.hp > 0 else False


@BaseUnit.register_group('formations', 'squad', 7000)
class BaseFormation(BaseUnit):
    """
    Can possibly extend unit's class with additional methods and properties,
    which can be applied only to formation-type unit (auras maybe, strategy type)
    Defined as group

    Squad has no such parameters as base_hp ahd bese_recharge_time, because
    group can be considered alive as long as there is at least one functional unit
    that belongs to that group

    Squad can attack is there is at least on unit that can attack at he moment
    (not on cd)
    """

    base_hp = None
    base_recharge_time = None

    def __init__(self, strategy=None, **kwargs):
        """
        Get params from kwargs, and call to base unit __init__ method
        """
        self.chosen_strategy = None
        super().__init__(**kwargs)

    def __repr__(self):
        string = super().__repr__()
        oper_hp = ' | '
        for unit in self.sub_units:
            print('sub_unit hp is', unit.hp)
            oper_hp += '{0:.3f}'.format(unit.hp) + ' | '
        return string + oper_hp

    def engage(self, defending_unit):
        return super().engage(defending_unit)

    @property
    def attack_damage(self):
        return None

    def attack_won(self):
        """
        Vehicle itself does not gets any additional bonuses from winning a battle
        But operators receive exp as a default infantry unit
        """
        for unit in self.sub_units:
            unit.attack_won()

    def attack_lost(self, damage):
        self.damage_receive(damage)

    def damage_receive(self, damage):
        """
        Deal equal damage to all subunits of a squad
        """
        damage_to_each = damage / len(self.sub_units)
        for unit in self.sub_units:
            unit.damage_receive(damage_to_each)

    def reload(self):
        self._last_attack_timestamp = self.scheduler()

    @property
    def attack_chance(self):
        """
        Soldiers attack success probability is calculated with following formula:
                    0.5 * (1 + health/100) * random(50 + experience, 100) / 100

        Note: because every unit has cooldown on attack, calculations performs only
        once per move
        """
        return self._attack_chance

    @attack_chance.setter
    def attack_chance(self, value):
        self._attack_chance = value

    def opponent_select(self, given_oponent=None):
        return given_oponent

    def attack_chance_calculate(self, initial=False):
        """
        Calculate a chance of a successful attack for a particular turn.
        'ready_to_attack_property' should be set to false explicitly, after calling this method
        (except if called in __init__)

        calculated by formula: 0.5 * (1 + vehicle.health / 100) * gavg(operators.attack_success),
                where gavg is geometric mean ((x1*x2*x3)^(1/3))

        :param initial:
        :return:
        """
        if self.ready_to_attack or initial and not self.is_prepared:
            average_atk_success = 1
            for operator in self.sub_units:
                average_atk_success = average_atk_success * operator.attack_chance
            average_atk_success = average_atk_success ** (1 / len(self.sub_units))
            self.attack_chance = 0.5 * (1 + self.hp / 100) * average_atk_success

    def ready_to_attack(self, current_time=None):
        if current_time is None:
            current_time = self.scheduler()
        # print(current_time - self.last_attack_timestamp)
        return True if current_time - self.last_attack_timestamp >= self.recharge_time else False

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
        for operator in self.sub_units:
            if not operator.is_alive:
                return False
        if self.hp <= 0:
            return False
        else:
            return True


if __name__ == '__main__':
    vehicle_1 = BaseUnit.new('dpv')
    vehicle_2 = BaseUnit.new('dpv')
