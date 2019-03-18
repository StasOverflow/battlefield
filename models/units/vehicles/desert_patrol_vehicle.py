from models.units.base_unit import BaseUnit
import random


# @BaseUnit.register('dpv')
class DPV(BaseUnit):
    """
    Stands for "desert patrol vehicle"
    """
    base_hp = 100
    base_recharge_time = 1000

    def __init__(self, addit_dict=None):
        self._vehicle_hp = 0
        if addit_dict is None:
            initial_hp = self.base_hp
            initial_cd = self.base_recharge_time
        else:
            initial_hp = addit_dict.pop('hp')
            initial_cd = addit_dict.pop('cd')
        super().__init__(hp=initial_hp, cd=initial_cd, units=addit_dict)

    def __repr__(self):
        return str(self.hp) + '+' + str(self.operator_hp_avg) + 'hp'

    @property
    def attack_damage(self):
        damage = 0
        for operator_index in range(len(self.sub_units)):
            operator_dmg = self.operator_xp_get(operator_index) / 100
            damage += operator_dmg
        return 0.1 + damage

    def damage_receive(self, damage):
        self.hp = self.hp - damage * 0.6
        for operator in self.sub_units:
            operator.hp = operator.hp - damage * 0.1

        lucky_one = random.choice(self.sub_units)
        lucky_one.hp = lucky_one.hp - damage * 0.1

    @property
    def attack_chance(self):
        average_atk_success = 1
        for operator in self.sub_units:
            average_atk_success = average_atk_success * operator.attack_chance
        average_atk_success = average_atk_success / len(self.sub_units)
        return 0.5 * (1 + self.hp / 100) * average_atk_success

    def is_ready_to_attack_at_the_moment(self, time):
        return True if time - self.last_attack_timestamp >= self.recharge_time else False

    def operator_xp_get(self, operator_index):
        return self.sub_units[operator_index].experience

    @property
    def operator_xp_total(self):
        total_xp = 0
        for operator_index, operator in enumerate(self.sub_units):
            if operator.is_alive:
                total_xp += self.operator_xp_get(operator_index)
        return total_xp

    def operator_hp_get(self, operator_index):
        return self.sub_units[operator_index].hp

    def operator_hp_set(self, operator_index, value):
        self.sub_units[operator_index].hp = value
        return

    @property
    def operator_hp_avg(self):
        oper_avg_hp = 0
        for oper_index in range(len(self.sub_units)):
            oper_avg_hp += self.operator_hp_get(oper_index)
        if oper_avg_hp is not 0:
            oper_avg_hp = oper_avg_hp / len(self.sub_units)
        return oper_avg_hp

    @property
    def vehicle_hp(self):
        return self._vehicle_hp

    @vehicle_hp.setter
    def vehicle_hp(self, value):
        self._vehicle_hp = value
        if self.vehicle_hp < 0:
            self._vehicle_hp = 0
        return

    @property
    def hp(self):
        return self.vehicle_hp

    @hp.setter
    def hp(self, value):
        self.vehicle_hp = value
        return

    @property
    def is_alive(self):
        alive_indicator = False
        if self.hp > 0 and self.operator_hp_avg > 0:
            alive_indicator = True
        return alive_indicator
