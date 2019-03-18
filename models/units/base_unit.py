from abc import ABC, abstractmethod


class Unit(ABC):

    UNIT = {}

    @classmethod
    def register(cls, name):
        def decorator(unit_cls):
            print("INSTANCE OF ", unit_cls)
            cls.UNIT[name] = unit_cls
            return unit_cls
        return decorator

    @classmethod
    def new(cls, name, addit_dict=None, **kwargs):
        return cls.UNIT[name](addit_dict, **kwargs)

    @abstractmethod
    def __init__(self, call_name, hp=0, cooldown=0, units=None):
        self._hp = 0

        self._sub_units = list()
        if units is not None:
            self.sub_units = units
        self.hp = hp
        self._call_name = call_name
        self._recharge_time = cooldown
        self._last_attack_timestamp = -self.recharge_time  # very cool workaround to attack instantly (kostil')

    def __repr__(self):
        type_of = self.__class__.__name__
        repr_string = type_of + ' | HP: ' + str(self.hp) \
                              + ' | DMG: ' + str(self.attack_damage) \
                              + ' | cd: ' + str(self.recharge_time) + ' |'
        return repr_string

    """Abstract methods and properties goes here"""
    # calculate attack damage of a unit, return 0 if attack chance fails
    @property
    @abstractmethod
    def attack_damage(self):
        pass

    # receive damage, specifically for a unit type
    @abstractmethod
    def damage_receive(self, damage):
        pass

    # calculate attack chance, specifically for a unit type
    @property
    @abstractmethod
    def attack_chance(self):
        pass

    # return either true or false, based on different parameters (unit-specific)
    @abstractmethod
    def is_ready_to_attack_at_the_moment(self, time):
        pass

    """Other unit properties, applied to all subclasses"""
    @property
    def sub_units(self):
        return self._sub_units

    @sub_units.setter
    def sub_units(self, units):
        # print(units)
        main_key = list(units.keys())[0]
        for unit in units[main_key]:
            self._sub_units.append(Unit.new(unit.pop('type'), unit))
        return

    # determines if unit is ready to attack
    @property
    def recharge_time(self):
        return self._recharge_time

    @recharge_time.setter
    def recharge_time(self, time):
        self._recharge_time = time
        return

    @property
    def last_attack_timestamp(self):
        return self._last_attack_timestamp

    @last_attack_timestamp.setter
    def last_attack_timestamp(self, time):
        self._last_attack_timestamp = time
        return

    @property
    def call_name(self):
        return self._call_name

    @call_name.setter
    def call_name(self, name):
        self._call_name = name
        return

    @property
    def hp(self):
        return self._hp

    @hp.setter
    @abstractmethod
    def hp(self, value):
        pass

    @property
    @abstractmethod
    def is_alive(self):
        pass
