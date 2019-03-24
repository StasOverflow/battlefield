import unittest
from models.combat.battle import get_unit_from_json


class TestVehicleMethods(unittest.TestCase):

    @staticmethod
    def sqaud_init():
        return get_unit_from_json("tests/test_squad.json")

    def setUp(self):
        self.squad = self.sqaud_init()

    def test_units_exits(self):
        self.assertTrue(len(self.squad.sub_units) > 0)

    def test_squad_sub_units_alive(self):
        for unit in self.squad.sub_units:
            self.assertTrue(unit.is_alive)

    def test_squad_sub_units_almost_dead(self):
        for unit in self.squad.sub_units:
            unit.hp = 0

        self.assertFalse(self.squad.is_alive)

    def test_squad_is_dead_or_almost_dead(self):
        self.squad.hp = 0
        self.assertFalse(self.squad.is_alive)
        for unit in self.squad.sub_units:
            unit.hp = 1
            if len(unit.sub_units):
                for sub_unit in unit.sub_units:
                    sub_unit.hp = 1
                    self.assertTrue(self.squad.is_alive)
                    sub_unit.hp = 0
                    self.assertFalse(self.squad.is_alive)
            else:
                self.assertTrue(self.squad.is_alive)
                unit.hp = 0
                self.assertFalse(self.squad.is_alive)


if __name__ == '__main__':
    unittest.main()
