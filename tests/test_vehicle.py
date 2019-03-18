import unittest
from models.units.base_unit import BaseUnit
import json


class TestVehicleMethods(unittest.TestCase):

    @staticmethod
    def vehicle_init():
        config_data_file = "tests/test_vehicle_cfg.json"
        if config_data_file is None:
            raise Exception('Something went wrong')
        else:
            with open(config_data_file) as conf:
                data = json.load(conf)
                print(data)
                unit_instance = BaseUnit.new(data.pop('type'), data)
        return unit_instance

    def test_is_alive(self):
        vehicle = self.vehicle_init()
        vehicle.damage_receive(400)
        self.assertFalse(vehicle.is_alive)

    def test_is_not_alive(self):
        vehicle = self.vehicle_init()
        vehicle.damage_receive(166.66666666666666666666667)
        print(vehicle)
        self.assertTrue(vehicle.is_alive)
    #
    # def test_damage_received_overwhelming(self):
    #     soldier = Soldier()
    #     soldier.damage_receive(400)
    #     self.assertEqual(soldier.hp, 0)
    #
    # def test_soldier_experience_overwhelming(self):
    #     soldier = Soldier()
    #     soldier.experience = 500
    #     self.assertEqual(soldier.experience, 50)
    #
    # def test_soldier_experience_negative(self):
    #     soldier = Soldier()
    #     soldier.experience = -400
    #     self.assertEqual(soldier.experience, 0)


if __name__ == '__main__':
    unittest.main()
