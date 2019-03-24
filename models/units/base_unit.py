from abc import ABC, abstractmethod
from random import choice
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
    :param: ready_to_attack() - Determine if unit's last attack was performed
            certain amount of time ago (where amount of time ago is even or more
            of unit's CD time)
    And more

    Unit group (formation for example) can be represented as follows:
        'formation***': {
            'units': (
                'unit_of_type_say_squad',
                'unit_of_type_say_medical_squad',
            )
            'depth': 3000
            TODO:
                'possible_subgroups': (
                    'infantry',
                    'vehicle',
                )
        }
    _____
    **
        An event is considered as attack event if unit's attack damage was called
        with purpose to participate in a battle
    ***
        Depth - depth is a value, determining a possibility of a certain unit-group
        to contain another units
        (unit with lower (say 2000) depth can contain a unit, which belongs to a
        deeper group (say 2001)).
    """
    def _attack_random(self, opponents_sub_units):
        # print('attacking random')
        alive_opponnent_list = [unit for unit in opponents_sub_units if unit.is_alive]
        if len(alive_opponnent_list):
            return choice(alive_opponnent_list)
        else:
            return False

    def _attack_weakest(self, opponents_sub_units):
        # print('attacking weakest')
        index_of_the_lowest = 0
        lowest_attack_chance = 0
        if len(opponents_sub_units):
            for index, unit in enumerate(opponents_sub_units):
                if unit.is_alive:
                    unit.attack_chance_calculate()
                    atk = unit.attack_chance
                    if lowest_attack_chance == 0:
                        lowest_attack_chance = atk
                        index_of_the_lowest = index
                    elif atk <= lowest_attack_chance:
                        lowest_attack_chance = atk
                        index_of_the_lowest = index
            return opponents_sub_units[index_of_the_lowest]
        else:
            return False

    def _attack_strongest(self, opponents_sub_units):
        # print('attacking strongest')
        index_of_the_highest = 0
        highest_attack_chance = 0
        if len(opponents_sub_units):
            for index, unit in enumerate(opponents_sub_units):
                if unit.is_alive:
                    unit.attack_chance_calculate()
                    atk = unit.attack_chance
                    if atk >= highest_attack_chance:
                        highest_attack_chance = atk
                        index_of_the_highest = index
            return opponents_sub_units[index_of_the_highest]
        else:
            return False

    STRATEGIES = {
        0: _attack_random,
        1: _attack_weakest,
        2: _attack_strongest,
    }

    GROUPS = {}

    scheduler = time.monotonic
    infantry_id = 0
    vehicle_id = 0
    squad_id = 0
    army_id = 0

    @classmethod
    def register_group(cls, group_name, unit_type, depth):
        """
        A factory, used for registering new unit classes
        // Is it a factory, anyways?
        :param group_name: A common name for group of alike units
        :param unit_type: Type of a unit
        :param depth: Value used to determine if unit can contain more units
            e.g.: unit with 9k depth can't contain unit with 8k depth,
        """
        def decorator(unit_cls):
            cls.GROUPS[group_name] = dict()
            cls.GROUPS[group_name]['units'] = dict()
            cls.GROUPS[group_name]['units'][unit_type] = unit_cls
            cls.GROUPS[group_name]['depth'] = depth
            return unit_cls
        return decorator

    @classmethod
    def new(cls, **kwargs):
        """
        Method that returns a class instance via its unit_type
        :param kwargs: params, passed to class
        :return: class instance
        """
        factory_class = None
        aydi = 0
        unit_type = kwargs.pop('type')
        for key, group_dict in cls.GROUPS.items():
            if unit_type in group_dict['units']:
                unit = group_dict['units'][unit_type]
                if inspect.isclass(unit) and issubclass(unit, cls):
                    factory_class = unit
                    if key == 'infantry':
                        cls.infantry_id += 1
                        aydi = cls.infantry_id
                    elif key == 'vehicle':
                        cls.vehicle_id += 1
                        aydi = cls.vehicle_id
                    elif key == 'formation':
                        cls.squad_id += 1
                        aydi = cls.squad_id
                    elif key == 'army':
                        cls.army_id += 1
                        aydi = cls.army_id
                    break
        if factory_class is None:
            raise AttributeError
        return factory_class(aydi=aydi, **kwargs)

    @abstractmethod
    def __init__(self, hp=None, cd=None, aydi=None, units=None, klass=None):
        self.id = aydi
        self._hp = 0
        self.depth = self.GROUPS[klass]['depth']
        self.sub_units = None
        self._sub_units = list()
        self.sub_units = units
        self.initial_hp = hp
        self.hp = self.initial_hp
        self._recharge_time = cd
        # very cool workaround to attack instantly (kostil')
        if cd is not None:
            self._last_attack_timestamp = self.scheduler()-self.recharge_time
        else:
            self._last_attack_timestamp = None
        self.attack_chance = None
        self.is_prepared = False
        self.attack_chance_calculate(initial=True)

    def __repr__(self):
        type_of = self.__class__.__name__
        dmg = '{0:.3f}'.format(self.attack_damage) if self.attack_damage is not None else 'None'
        cd = '{0:.3f}'.format(self.recharge_time) if self.recharge_time is not None else 'None'
        chance = '{0:.3f}'.format(self.attack_chance) if self.attack_chance is not None else '0'
        ready_to_attack = str(self.ready_to_attack()) if self.ready_to_attack() is not None else '0'
        stats_string = ' | DMG: ' + dmg \
                       + ' | cd: ' + cd \
                       + ' | atk: ' + chance \
                       + ' | rdy: ' + ready_to_attack
        if not self.is_alive:
            stats_string = ' | DECEASED '
        repr_string = type_of + ' | ID :' + str(self.id) \
                              + ' | HP: ' + '{0:.3f}'.format(self.hp) \
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
            self.attack_chance_calculate()
            defending_unit.attack_chance_calculate()
            self.reload()
            atk_side_chance = self.attack_chance
            def_side_chance = defending_unit.attack_chance
            self.is_prepared = False
            if atk_side_chance > def_side_chance:
                self.attack_won()
                defending_unit.attack_lost(self.attack_damage)
                return True
            else:
                return False
        else:
            return False

    @abstractmethod
    def opponent_select(self, given_opponent=None):
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
    def ready_to_attack(self):
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
        if units is not None:
            if isinstance(units, list):
                for unit_data in units:
                    self._sub_units.append(BaseUnit.new(**unit_data))

    def sub_units_insert(self, explicit_array, json=False):
        if json:
            self.sub_units = explicit_array
        if explicit_array is not None:
            for unit in explicit_array:
                self._sub_units.append(unit)

    @property
    def recharge_time(self):
        return self._recharge_time

    @recharge_time.setter
    def recharge_time(self, rec_time):
        self._recharge_time = rec_time
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
