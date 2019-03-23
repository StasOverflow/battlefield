import unittest
from models.units.base_unit import BaseUnit
import json


class TestVehicleMethods(unittest.TestCase):

    @staticmethod
    def vehicle_init():
        config_data_file = "tests/test_vehicle.json"
        if config_data_file is None:
            raise Exception('Missing config file for vehicle!')
        else:
            with open(config_data_file) as conf:
                data = json.load(conf)
                # type_of = data.pop('type')
                unit_instance = BaseUnit.new(**data)
        return unit_instance

    def setUp(self):
        self.vehicle = self.vehicle_init()

    def test_is_alive(self):
        self.vehicle.damage_receive(500)
        self.assertFalse(self.vehicle.is_alive)

    def test_is_not_alive(self):
        self.vehicle.damage_receive(166.66666666666666666666667)
        self.assertTrue(self.vehicle.is_alive)

    def test_soldier_on_cooldown(self):
        enemy = self.vehicle_init()
        self.assertTrue(self.vehicle.ready_to_attack())
        self.assertTrue(enemy.ready_to_attack())
        self.vehicle.engage(enemy)
        self.assertFalse(self.vehicle.ready_to_attack())
        self.assertTrue(enemy.ready_to_attack())


if __name__ == '__main__':
    unittest.main()
