from abc import ABC, abstractmethod
import inspect
import time

time.monotonic()


class BaseUnit(ABC):
    """
    Base unit class for all units, taking part in a battle

    Every unit has its:
    :param: HP - Hit Pointes
    :param: CD - Cooldown
    :param: attack_chance - Unit's chance of a successful attack
            Note: a param is compared to units counterpart, to
            determine if damage will or will not be done
    :param: attack_damage - Unit's attack damage
    :param: is_prepared - A flag, that indicates if Unit's attack_chance
            has already been calculated;
            Note: should be set to False explicitly after every attack event**
    :param: ready_to_attack(time) - Determine if unit's last attack was performed
            certain amount of time ago (where amount of time is value of current
            time minus CD)
    And more
    _____
    ** An event is considered as attack event if unit's attack damage was called
       with purpose to participate in a battle
    """
    GROUPS = {}

    scheduler = time.monotonic
    infantry_id = 0

    @classmethod
    def register_group(cls, group_name, unit_type, depth):
        """
        A factory, used for registering new unit classes
        // Is it a factory, anyways?
        :param group_name: A common name for group of alike units
        :param unit_type: Type of a unit
        :param depth: Value used to determine if unit can contain more units
                      e.g.: unit with 9k depth can't contain unit with 8k depth,
                            cant attack units with 8k depth, and so on
        """
        def decorator(unit_cls):
            cls.GROUPS[group_name] = dict()
            cls.GROUPS[group_name][unit_type] = unit_cls
            cls.GROUPS[group_name]['depth'] = depth
            return unit_cls
        return decorator

    @classmethod
    def new(cls, unit_type, **kwargs):
        """
        Method that returns a class instance via its unit_type
        :param unit_type: code name of a class, defined via '@register_group(gn, unit_type, 300)'
        :param kwargs: params, passed to class
        :return: class instance
        """
        factory_class = None
        depth = None
        for key, group_dict in cls.GROUPS.items():
            for sub_key, item in group_dict.items():
                if inspect.isclass(item) and issubclass(item, cls):
                    if sub_key == unit_type:
                        factory_class = item
                        depth = group_dict['depth']
                        break
        if factory_class is None:
            raise AttributeError
        cls.infantry_id += 1
        return factory_class(depth=depth, aydi=cls.infantry_id, **kwargs)

    @abstractmethod
    def __init__(self, hp=0, cd=0, aydi=None, units=None, depth=None):
        self.id = aydi
        self._hp = 0
        self.depth = depth
        self._sub_units = list()
        if units is not None:
            self.sub_units = units
        self.initial_hp = hp
        self.hp = self.initial_hp
        self._recharge_time = cd
        self._last_attack_timestamp = self.scheduler()-self.recharge_time  # very cool workaround to attack instantly (kostil')
        self.attack_chance = None
        self.is_prepared = False
        self.attack_chance_calculate(initial=True)

    def __repr__(self):
        type_of = self.__class__.__name__
        stats_string = ' | DMG: ' + str(self.attack_damage) \
                       + ' | cd: ' + str(self.recharge_time) \
                       + ' | atk: ' + str(self.attack_chance) \
                       + ' | rdy: ' + str(self.ready_to_attack(self.scheduler()))
        if not self.is_alive:
            stats_string = ' | DECEASED '
        repr_string = type_of + ' | ID :' + str(self.id) \
                              + ' | HP: ' + str(self.hp) \
                              + stats_string
        return repr_string

    '''
    Abstract methods and properties goes here
    '''
    @abstractmethod
    def engage(self, defending_unit):
        """
        Performs the following:
            -calculates successful attack probability form each of battling sides
            -sets 'prepared' property of attacking unit to False, allowing to recalculate
             attack chance on the next engagement
            -performs an attack if attacking side unit's attack chance is more than
             defending side unit's one (by triggering attack_won|lost methods)
            -starts cooldown for attacking unit

        :param defending_unit:
        :return: True if attack performed, False otherwise
        """
        if self.ready_to_attack():
            defending_unit = self.opponent_select(defending_unit)
            self.is_prepared = False
            atk_side_chance = self.attack_chance
            def_side_chance = defending_unit.attack_chance
            if atk_side_chance > def_side_chance:
                self.attack_won()
                defending_unit.attack_lost(self.attack_damage)
            self.reload()
            return True
        else:
            return False

    @abstractmethod
    def opponent_select(self, given_oponent=None):
        """
        Selects an opponent, according to chosen tactics
        :return:
        """
        pass

    @property
    @abstractmethod
    def attack_damage(self):
        """
        Calculate attack damage of a unit
        :return: Attack damage of a unit, if attack succeeds
        """
        pass

    @abstractmethod
    def damage_receive(self, damage):
        """
        Receive damage, each unit receive damage differently, based on its type
        e.g.: can be spread, if dealt to squad
        """
        pass

    @property
    @abstractmethod
    def attack_chance(self):
        """
        :return Calculated value of a succesful attack for current move
        """
        pass

    @attack_chance.setter
    @abstractmethod
    def attack_chance(self, value):
        """
        Set a chance of a successful attack for particular move (until reload)
        """
        self._attack_chance = value

    @abstractmethod
    def attack_chance_calculate(self, initial=False):
        pass

    @property
    @abstractmethod
    def hp(self):
        """
        Hit-points of a certain unit
        """
        return self._hp

    @hp.setter
    @abstractmethod
    def hp(self, value):
        pass

    @property
    @abstractmethod
    def is_alive(self):
        """
        We usually consider unit as dead (or inactive) if it's hp <= 0%
        """
        pass

    @abstractmethod
    def attack_won(self):
        pass

    @abstractmethod
    def attack_lost(self, damage):
        pass

    @abstractmethod
    def ready_to_attack(self, current_time=None):
        """
        Determines if unit is ready to attack
        """
        pass

    '''
    Other unit properties, applied to all subclasses
    '''
    @property
    def is_prepared(self):
        """
        Determines if unit performed its successful attack probability calculations for a particular move
        """
        return self._is_prepared

    @is_prepared.setter
    def is_prepared(self, value):
        """
        Should be reset to False every attack (or every every event from above classes, that triggers
        damage & chance properties)
        """
        self._is_prepared = value

    @property
    def sub_units(self):
        return self._sub_units

    @sub_units.setter
    def sub_units(self, units):
        """
        Accepts a certain json-like object, which determines what units
        will be considered as sub-units of this unit (not that hard as it sounds)
        :param units: json like object with sub-unit (or sub-units) param(s)
                e.g.:
                    {
                        "type": "necromancer",
                        "hp": 300,
                        "cd": 881,
                        "name": "Gul`Dan"
                    },
                    {
                        "type": "soldier",
                        "hp": 100,
                        "cd": 963,
                        "name": "Steve"
                    },
        """
        # print(units)
        main_key = list(units.keys())[0]
        print(main_key)
        for unit in units[main_key]:
            self._sub_units.append(BaseUnit.new(unit.pop('type'), unit))

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
    def last_attack_timestamp(self, new_time):
        self._last_attack_timestamp = new_time
        return

    @abstractmethod
    def reload(self):
        pass

    """
    Just an idea, would be cool to generate call names of soldiers,
    squads, etc either from json, or somehow else
    @property
    def call_name(self):
        return self._call_name

    @call_name.setter
    def call_name(self, name):
        self._call_name = name
        return
    """

    @property
    def hp_percentage(self):
        """
        Same as hit points, but as percent of base hit points
        :return: percents of hp left
        """
        return self.hp / self.initial_hp * 100
