from models.units.base_unit import BaseUnit
import random


@BaseUnit.register_group('infantry', 'soldier', 9000)
class BaseInfantry(BaseUnit):
    """
    Can possibly extend unit's class with additional methods and properties,
    which can be applied only to infantry-type unit (like special equipment)
    Defined as soldier

    :param base_hp: base hp of a default infantry unit, used it none specified
    :param base_recharge_time: base recharge_time, same as above
    """

    base_hp = 100
    base_recharge_time = .200

    def __init__(self, **kwargs):
        """
        Get params from kwargs, and call to base unit __init__ method
        """
        self.hp = 0
        stats = kwargs.get('stats')
        if stats is None:
            initial_hp = self.base_hp
            initial_cd = self.base_recharge_time
        else:
            initial_hp = stats.pop('hp')
            initial_cd = stats.pop('cd')
        self.experience = 0
        super().__init__(hp=initial_hp, cd=initial_cd, **kwargs)

    def __repr__(self):
        string = super().__repr__()
        return string + ' | EXP : ' + str(self.experience)

    def engage(self, defending_unit):
        return super().engage(defending_unit)

    @property
    def attack_damage(self):
        attack_damage = 0
        if self.is_alive:
            attack_damage = 0.05 + self.experience / 100
        return attack_damage

    def attack_won(self):
        self.experience_increase()

    def attack_lost(self, damage):
        self.damage_receive(damage)

    def damage_receive(self, damage):
        self.hp = self.hp - damage

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

        Note: Method has a slight malfunctioning, because attacking side calls it twice
        on the first turn (first in __init__ method, second - before attack)

        :param initial:
        :return:
        """
        if self.ready_to_attack or initial and not self.is_prepared:
            self.is_prepared = True
            self.attack_chance = 0.5 * (1 + self.hp / 100) * random.randint(50 + self.experience, 100) / 100

    def ready_to_attack(self, current_time=None):
        if current_time is None:
            current_time = self.scheduler()
        # print(current_time - self.last_attack_timestamp)
        return True if current_time - self.last_attack_timestamp >= self.recharge_time else False

    @property
    def experience(self):
        """
        A property, that increments on each successful attack (increases damage)
        """
        if self.is_alive:
            experience = self._experience
        else:
            experience = 0
        return experience

    @experience.setter
    def experience(self, exp_value):
        if self.experience >= 50:
            self._experience = 50
        elif self.experience <= 0:
            self._experience = 0
        self._experience = exp_value

    def experience_increase(self, success=True):
        if success:
            exp = self.experience
            self.experience = exp + 1
            print(self.experience)

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
        return True if self.hp > 0 else False