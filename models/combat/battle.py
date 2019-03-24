from models.units.base_unit import BaseUnit
import json
import time


def get_unit_from_json(json_file):
    if json_file is None:
        raise Exception('Missing config file for unit!')
    else:
        with open(json_file) as conf:
            data = json.load(conf)
            unit_instance = BaseUnit.new(**data)
    return unit_instance


def get_cfg_from_json(json_file):
    if json_file is None:
        raise Exception('Missing config file for unit!')
    else:
        with open(json_file) as conf:
            armies = list()
            data = json.load(conf)
            for unit_data in data['armies']:
                unit = BaseUnit.new(**unit_data)
                armies.append(unit)
            return armies


class Battle:
    setup = {}

    def __init__(self, incoming_config=None):
        self._participants = get_cfg_from_json(incoming_config)
        self.current_attacker_index = 0
        self._log_timestamp = time.monotonic()

        for unit in self._participants:
            print(unit)

    def next_alive_unit(self, index):
        defending_unit_index = index + 1
        if defending_unit_index > (len(self._participants) - 1):
            defending_unit_index = 0
        print('attacker is ', self.current_attacker_index, ' on', defending_unit_index)
        if self._participants[defending_unit_index].is_alive:
            return defending_unit_index
        else:
            if defending_unit_index != self.current_attacker_index:
                return False
            else:
                return self.next_alive_unit(defending_unit_index)

    def clockwise_attack(self):
        defending_unit_index = self.next_alive_unit(self.current_attacker_index)
        if defending_unit_index:
            # print(
            self._participants[self.current_attacker_index].engage(self._participants[defending_unit_index])
            self.current_attacker_index = self.next_alive_unit(self.current_attacker_index)

    def winner_get(self):
        alive_unit_count = 0
        for index, unit in enumerate(self._participants):
            if unit.is_alive:
                alive_unit_count += 1
                alive_index = index
        if alive_unit_count == 1:
            return self._participants[alive_index]
        else:
            return False

    def battle_log_schedule(self, every):
        cur_time = time.monotonic()
        if cur_time - self._log_timestamp >= every:
            self._log_timestamp = cur_time
            print(self.battle_log_get())

    def battle_log_get(self):
        string = 'battle_status: \n'
        for unit in self._participants:
            string += str(unit) + '\n'
        string += '_' * 80
        return string

