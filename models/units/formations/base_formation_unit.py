from models.units.base_unit import BaseUnit


@BaseUnit.register_group('formation', 'squad', 7000)
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
        type_of = self.__class__.__name__
        chance = '{0:.3f}'.format(self.attack_chance) if self.attack_chance is not None else '0'
        ready_to_attack = str(self.ready_to_attack()) if self.ready_to_attack() is not None else '0'
        stats_string = ' | Chance: ' + chance \
                       + ' | rdy: ' + ready_to_attack
        if not self.is_alive:
            stats_string = ' | DECEASED '
        repr_string = type_of + ' | ID :' + str(self.id) \
                              + stats_string
        sub_unit_hp = ' | '
        for unit in self.sub_units:
            if unit.is_alive:
                sub_unit_hp += '{0:.3f}'.format(unit.hp) + ' ' + str(unit.ready_to_attack()) + ' | '
            else:
                sub_unit_hp += 'DECEASED | '
        return repr_string + sub_unit_hp

    def engage(self, defending_unit):
        if self.ready_to_attack():
            defending_unit = self.opponent_select(defending_unit)
            self.attack_chance_calculate()
            defending_unit.attack_chance_calculate()
            atk_side_chance = self.attack_chance
            def_side_chance = defending_unit.attack_chance
            if atk_side_chance > def_side_chance:
                self.attack_won()
                defending_unit.damage_receive(self.attack_damage)
                return True
            else:
                return False
        else:
            return False

    @property
    def attack_damage(self):
        """
        As squad itself attacks with its subunits, we consider the fact of summoning attack
        damage getter as if unit attacks, and attack should be followed by calling to reload()
        """
        acc_damage = 0
        for unit in self.sub_units:
            if unit.ready_to_attack():
                acc_damage += unit.attack_damage
                unit.reload()
        return acc_damage

    def attack_won(self):
        """
        Squad units operates as coherent group, so winning a battle provides bonuses for
        all units in a squad
        """
        for unit in self.sub_units:
            unit.attack_won()

    def attack_lost(self, damage):
        self.damage_receive(damage)

    def damage_receive(self, damage):
        """
        Squad units operates as coherent group, so losing a battle affects all units inside
        of a formation (with a same amount of damage)
        """
        alive_units = [unit for unit in self.sub_units if unit.is_alive]
        damage_to_each = damage / len(alive_units)
        print('dealing ', damage_to_each, ' to ', len(alive_units), ' units')
        if len(alive_units):
            for unit in alive_units:
                unit.damage_receive(damage_to_each)

    def reload(self):
        pass

    @property
    def attack_chance(self):
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

        calculated by formula: gavg(sub_unit.attack_success),
                where gavg is geometric mean ((x1*x2..xN)^(1/N))

        :param initial:
        :return:
        """
        if self.ready_to_attack() or initial:
            average_atk_success = 1
            # print(self.sub_units)
            for unit in self.sub_units:
                if unit.ready_to_attack():
                    unit.attack_chance_calculate()
                    average_atk_success = average_atk_success * unit.attack_chance
            average_atk_success = average_atk_success ** (1/len(self.sub_units))
            self.attack_chance = average_atk_success

    def ready_to_attack(self):
        """
        A formation is ready to attack if at least one unit in a formation is ready
        to attack
        """
        if self.is_alive:
            for unit in self.sub_units:
                if unit.ready_to_attack():
                    return True
            return False
        else:
            return False

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
        units_dead = 0
        for unit in self.sub_units:
            if not unit.is_alive:
                units_dead += 1
        if units_dead == len(self.sub_units):
            return False
        else:
            return True


"""

    def __repr__(self):
        string = super().__repr__()
        oper_hp = ' | '
        for operator in self.sub_units:
            oper_hp += '{0:.3f}'.format(operator.hp) + ' | '
        return string + oper_hp

    def engage(self, defending_unit):
        return super().engage(defending_unit)

    @property
    def attack_damage(self):
        damage = 0
        for operator in self.sub_units:
            operator_dmg = operator.experience / 100
            damage += operator_dmg
        return 0.1 + damage

    def attack_won(self):
        Vehicle itself does not gets any additional bonuses from winning a battle
        But operators receive exp as a default infantry unit
        
        for operator in self.sub_units:
            operator.attack_won()

    def attack_lost(self, damage):
        self.damage_receive(damage)

    def damage_receive(self, damage):
        Damage received applies not only to vehicle, but spread among operators as well

        Vehicle gets 60% of total damage
        Luckiest operator gets 20% of total damage (receives 10% of damage twice)
        Other operators takes 10% of total damage
        
        self.hp = self.hp - damage * 0.6
        for operator in self.sub_units:
            operator.damage_receive(damage * 0.1)

        lucky_one = random.choice(self.sub_units)
        lucky_one.damage_receive(damage * 0.1)

    def reload(self):
        self._last_attack_timestamp = self.scheduler()

    @property
    def attack_chance(self):
    
        Soldiers attack success probability is calculated with following formula:
                    0.5 * (1 + health/100) * random(50 + experience, 100) / 100

        Note: because every unit has cooldown on attack, calculations performs only
        once per move
        
        return self._attack_chance

    @attack_chance.setter
    def attack_chance(self, value):
        self._attack_chance = value

    def opponent_select(self, given_opponent=None):
        return given_opponent

    def attack_chance_calculate(self, initial=False):
        Calculate a chance of a successful attack for a particular turn.
        'ready_to_attack_property' should be set to false explicitly, after calling this method
        (except if called in __init__)

        calculated by formula: 0.5 * (1 + vehicle.health / 100) * gavg(operators.attack_success),
                where gavg is geometric mean ((x1*x2*x3)^(1/3))

        :param initial:
        :return:

        if self.ready_to_attack() or (initial and not self.is_prepared):
            self.is_prepared = True
            average_atk_success = 1
            # print(self.sub_units)
            for operator in self.sub_units:
                operator.attack_chance_calculate()
                average_atk_success = average_atk_success * operator.attack_chance
            average_atk_success = average_atk_success ** (1/len(self.sub_units))
            self.attack_chance = 0.5 * (1 + self.hp / 100) * average_atk_success

    def ready_to_attack(self):
        current_time = self.scheduler()
        is_ready = True if current_time - self.last_attack_timestamp >= self.recharge_time else False
        return is_ready

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
        operators_dead = 0
        for operator in self.sub_units:
            if not operator.is_alive:
                operators_dead += 1
        if self.hp <= 0 or operators_dead == len(self.sub_units):
            return False
        else:
            return True
"""


if __name__ == '__main__':
    group_one = get_unit_from_json('tests/test_squad.json')
    group_two = get_unit_from_json('tests/test_squad.json')
    vice_versa = 0
    for i in range(50000000):
        if vice_versa:
            attack = group_one.engage(group_two)
        else:
            attack = group_two.engage(group_one)
        vice_versa = not vice_versa
        # if attack:
        #     print('round result: \n', str(group_one), '\n', str(group_two), '\n', '_'*80)

