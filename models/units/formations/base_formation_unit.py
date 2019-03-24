from models.units.base_unit import BaseUnit
from models.combat.logging_cfg import battle_logger
import time


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
        hp = '{0:.3f}'.format(self.hp)
        stats_string = ' | HP: ' + str(hp) + ' | Chance: ' + chance + ' | rdy: ' + ready_to_attack
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
            battle_logger.info(time.monotonic(), self, 'is ready to attack')
            defending_unit = self.opponent_select(defending_unit)
            self.attack_chance_calculate()
            if defending_unit is not None:
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
        battle_logger.info(time.monotonic(), self, 'receiving damage')
        alive_units = [unit for unit in self.sub_units if unit.is_alive]
        if len(alive_units):
            damage_to_each = damage / len(alive_units)
            # print('dealing ', damage_to_each, ' to ', len(alive_units), ' units')
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
        """
        :return: Sum of sub-units hps
        """
        hp = 0
        for unit in self.sub_units:
            hp += unit.hp
        return hp

    @hp.setter
    def hp(self, value):
        """
        Accepts only zero value, meaning unit is dead
        """
        if value == 0:
            for unit in self.sub_units:
                unit.hp = 0
        return

    @property
    def is_alive(self):
        units_dead = 0
        for unit in self.sub_units:
            if not unit.is_alive:
                units_dead += 1
        # print(units_dead, len(self.sub_units))
        if units_dead == len(self.sub_units):
            return False
        else:
            return True
