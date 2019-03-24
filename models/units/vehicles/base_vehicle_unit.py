from models.units.base_unit import BaseUnit
import random


@BaseUnit.register_group('vehicle', 'dpv', 8000)
class BaseVehicle(BaseUnit):
    """
    Can possibly extend unit's class with additional methods and properties,
    which can be applied only to vehicle-type unit (like vehicle type,
    bow-gun-type, etc)
    Defined as desert patrol vehicle

    :param base_hp: base hp of a default vehicle unit, used it none specified
    :param base_recharge_time: base recharge_time, same as above
    """

    base_hp = 500
    base_recharge_time = 0.1

    def __init__(self, **kwargs):
        """
        Get params from kwargs, and call to base unit __init__ method
        """
        super().__init__(**kwargs)

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
        alive_units = [unit for unit in self.sub_units if unit.is_alive]
        for unit in alive_units:
            operator_dmg = unit.experience / 100
            damage += operator_dmg
        return 0.1 + damage

    def attack_won(self):
        """
        Vehicle itself does not gets any additional bonuses from winning a battle
        But operators receive exp as a default infantry unit
        """
        alive_units = [unit for unit in self.sub_units if unit.is_alive]
        for unit in alive_units:
            unit.attack_won()

    def attack_lost(self, damage):
        self.damage_receive(damage)

    def damage_receive(self, damage):
        """
        Damage received applies not only to vehicle, but spread among operators as well

        Vehicle gets 60% of total damage
        Luckiest operator gets 20% of total damage (receives 10% of damage twice)
        Other operators takes 10% of total damage
        """
        self.hp = self.hp - damage * 0.6
        alive_units = [unit for unit in self.sub_units if unit.is_alive]
        if len(alive_units):
            for unit in alive_units:
                unit.damage_receive(damage * (0.3 / len(alive_units)))

            lucky_one = random.choice(alive_units)
            lucky_one.damage_receive(damage * 0.1)

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
        return self._attack_chance if self.is_alive else False

    @attack_chance.setter
    def attack_chance(self, value):
        self._attack_chance = value

    def opponent_select(self, given_opponent=None):
        return given_opponent

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
        return is_ready if self.is_alive else False

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if self._hp <= 0:
            self._hp = 0
            for unit in self.sub_units:
                unit.hp = 0
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
