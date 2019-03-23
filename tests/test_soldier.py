import unittest
from models.combat.battle import get_unit_from_json


class TestSoldierMethods(unittest.TestCase):

    @staticmethod
    def soldier_init():
        return get_unit_from_json("tests/test_soldier.json")

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

    def test_soldier_attack_chance_when_dead(self):
        self.soldier.hp = 0
        self.soldier.attack_chance_calculate()
        self.assertFalse(self.soldier.is_alive)
        self.assertEqual(self.soldier.attack_chance, 0)


if __name__ == '__main__':
    unittest.main()
