import unittest
from models.combat.battle import get_unit_from_json


class TestVehicleMethods(unittest.TestCase):

    @staticmethod
    def army_init():
        return get_unit_from_json("tests/test_army.json")

    def setUp(self):
        self.army = self.army_init()

    def test_units_exits(self):
        self.assertTrue(len(self.army.sub_units) > 0)

    def test_army_sub_units_alive(self):
        for unit in self.army.sub_units:
            self.assertTrue(unit.is_alive)

    def test_army_sub_units_dead(self):
        for unit in self.army.sub_units:
            unit.hp = 0
        self.assertFalse(self.army.is_alive)

    def test_army_sub_units_almost_dead(self):
        new_units_list = self.army.sub_units[:-1]
        for unit in new_units_list:
            unit.hp = 0
        self.assertTrue(self.army.is_alive)
        self.army.sub_units[-1].hp = 0
        self.assertFalse(self.army.is_alive)

    # def test_army_attack_another_army(self):
    #     import io
    #     import sys
    #     opponent = get_unit_from_json("tests/test_army.json")
    #
    #     self.army.chosen_strategy = 0
    #     output = io.StringIO()
    #     sys.stdout = output
    #     self.army.engage(opponent)
    #     self.assertIn('attacking random', output.getvalue())
    #     sys.stdout = sys.__stdout__
    #
    #     self.army.chosen_strategy = 1
    #     output = io.StringIO()
    #     sys.stdout = output
    #     self.army.engage(opponent)
    #     self.assertIn('attacking weakest', output.getvalue())
    #     sys.stdout = sys.__stdout__
    #
    #     self.army.chosen_strategy = 2
    #     output = io.StringIO()
    #     sys.stdout = output
    #     self.army.engage(opponent)
    #     self.assertIn('attacking strongest', output.getvalue())
    #     sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
