import unittest
from models.combat.battle import get_unit_from_json


class TestVehicleMethods(unittest.TestCase):

    @staticmethod
    def vehicle_init():
        return get_unit_from_json("tests/test_vehicle.json")

    def setUp(self):
        self.vehicle = self.vehicle_init()

    def test_operators_exits(self):
        self.assertEqual(len(self.vehicle.sub_units), 3)

    def test_is_not_alive(self):
        self.vehicle.damage_receive(5000)
        self.assertFalse(self.vehicle.is_alive)

    def test_is_alive(self):
        self.vehicle.damage_receive(166.66666666666666666666667)
        self.assertTrue(self.vehicle.is_alive)

    def test_is_alive_with_one_operator(self):
        self.vehicle.sub_units[0].hp = 0
        self.vehicle.sub_units[1].hp = 0
        self.vehicle.sub_units[2].hp = 1
        self.assertTrue(self.vehicle.is_alive)

    def test_is_not_alive_with_no_one_alive(self):
        self.vehicle.sub_units[0].hp = 0
        self.vehicle.sub_units[1].hp = 0
        self.vehicle.sub_units[2].hp = 0
        self.assertFalse(self.vehicle.is_alive)

    def test_soldier_on_cooldown(self):
        enemy = self.vehicle_init()
        self.assertTrue(self.vehicle.ready_to_attack())
        self.assertTrue(enemy.ready_to_attack())
        self.vehicle.engage(enemy)
        self.assertFalse(self.vehicle.ready_to_attack())
        self.assertTrue(enemy.ready_to_attack())


if __name__ == '__main__':
    unittest.main()
