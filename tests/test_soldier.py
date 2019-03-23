import unittest
from models.units.base_unit import BaseUnit
import json


class TestSoldierMethods(unittest.TestCase):

    @staticmethod
    def soldier_init():
        config_data_file = "tests/test_soldier.json"
        if config_data_file is None:
            raise Exception('Missing config file for soldier!')
        else:
            with open(config_data_file) as conf:
                data = json.load(conf)
                # type_of = data.pop('type')
                unit_instance = BaseUnit.new(**data)
        return unit_instance

    def setUp(self):
        self.soldier = self.soldier_init()

    def test_is_alive(self):
        self.assertTrue(self.soldier.is_alive)

    def test_is_not_alive(self):
        self.soldier.damage_receive(9000)
        self.assertFalse(self.soldier.is_alive)
        self.assertEqual(self.soldier.attack_damage, 0)

    def test_damage_received(self):
        self.assertEqual(self.soldier.hp, 100)
        self.soldier.damage_receive(400)
        self.assertNotEqual(self.soldier.hp, 100)

    def test_soldier_experience_overflow(self):
        self.soldier.experience = 500
        self.assertEqual(self.soldier.experience, 50)

    def test_soldier_experience_underflow(self):
        self.soldier.experience = -400
        self.assertEqual(self.soldier.experience, 0)

    def test_soldier_on_cooldown(self):
        enemy = self.soldier_init()
        self.assertTrue(self.soldier.ready_to_attack())
        self.assertTrue(enemy.ready_to_attack())
        self.soldier.engage(enemy)
        self.assertFalse(self.soldier.ready_to_attack())
        self.assertTrue(enemy.ready_to_attack())


if __name__ == '__main__':
    unittest.main()
