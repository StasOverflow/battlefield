import unittest
from models.units.infantry.base_infantry_unit import BaseInfantry


class TestSoldierMethods(unittest.TestCase):

    def setUp(self):
        self.soldier = BaseInfantry()

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
        enemy = BaseInfantry()
        self.assertTrue(self.soldier.ready_to_attack())
        self.assertTrue(enemy.ready_to_attack())
        self.soldier.engage(enemy)
        self.assertFalse(self.soldier.ready_to_attack())
        self.assertTrue(enemy.ready_to_attack())


if __name__ == '__main__':
    unittest.main()
