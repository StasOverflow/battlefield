from abc import ABC, abstractmethod


class Unit(ABC):

    _base_hp = 0

    UNIT = {}

    @classmethod
    def base_hp(cls):
        return cls._base_hp

    @abstractmethod
    def __init__(self, call_name, hp=0, cooldown=0, units=None):
        self.hp = hp
        self.call_name = call_name
        self._recharge_time = cooldown
        self._last_attack_timestamp = -self.recharge_time  # very cool workaround to attack instantly (kostil')
        self._is_ready_to_attack = 0
        if units is not None:
            self.sub_units = units

    @property
    def last_attack_timestamp(self):
        return self._last_attack_timestamp

    @last_attack_timestamp.setter
    def last_attack_timestamp(self, time):
        self._last_attack_timestamp = time
        return

    @property
    def sub_units(self):
        return self._sub_units

    @sub_units.setter
    def sub_units(self, units):
        # print(units)
        self._sub_units = list()
        main_key = list(units.keys())[0]
        for unit in units[main_key]:
            self._sub_units.append(Unit.new(unit.pop('type'), unit))
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
    def hp(self, value):
        self._hp = value
        return

    @abstractmethod
    def damage_receive(self, damage):
        pass

    @property
    @abstractmethod
    def attack_damage(self):
        pass

    @property
    @abstractmethod
    def attack_chance(self):
        pass

    @property
    def is_alive(self):
        return True if self.hp > 0 else False

    @property
    @abstractmethod
    def is_ready_to_attack(self):
        pass

    @is_ready_to_attack.setter
    @abstractmethod
    def is_ready_to_attack(self, time):
        pass

    @property
    def recharge_time(self):
        return self._recharge_time

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

    def __repr__(self):
        type_of = self.__class__.__name__
        repr_string = type_of + ' | HP: ' + str(self.hp) \
                              + ' | DMG: ' + str(self.attack_damage) \
                              + ' | cd: ' + str(self.recharge_time) + ' |'
        # print(repr_string)
        return repr_string

