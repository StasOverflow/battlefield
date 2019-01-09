from abc import ABC, abstractmethod


class Unit(ABC):

    _base_hp = 0

    @classmethod
    def base_hp(cls):
        return cls._base_hp

    @abstractmethod
    def __init__(self, hp, cooldown_time):
        self._hp = hp
        self._base_cd = cooldown_time
        self._cd_status = self._base_cd

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        return

    # @property
    # @abstractmethod
    # def damage(self):
    #     pass
    #
    # @damage.setter
    # @abstractmethod
    # def damage(self, value):
    #     pass
    #
    # @property
    # @abstractmethod
    # def atk_success(self):
    #     pass
    #
    # @atk_success.setter
    # @abstractmethod
    # def atk_success(self, value):
    #     pass

    UNIT = {}

    @classmethod
    def register(cls, name):
        def decorator(unit_cls):
            cls.UNIT[name] = unit_cls
            return unit_cls
        return decorator

    @classmethod
    def new(cls, name, **kwargs):
        return cls.UNIT[name](**kwargs)

    def __repr__(self):
        type_of = self.__class__.__name__
        repr_string = type_of + ' | HP: ' + str(self.hp) \
                              + ' | DMG: ' + str(self.damage) \
                              + ' | cd: ' + str(self.cooldown) + ' |'
        # print(repr_string)
        return repr_string

