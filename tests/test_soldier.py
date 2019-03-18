import unittest
from models.units.infantry import Soldier


class TestSoldierMethods(unittest.TestCase):

    def test_is_alive(self):
        soldier = Soldier()
        self.assertTrue(soldier.is_alive)

    def test_is_not_alive(self):
        soldier = Soldier()
        soldier.hp = 0
        self.assertFalse(soldier.is_alive)

    def test_damage_received_overwhelming(self):
        soldier = Soldier()
        soldier.damage_receive(400)
        self.assertEqual(soldier.hp, 0)

    def test_soldier_experience_overwhelming(self):
        soldier = Soldier()
        soldier.experience = 500
        self.assertEqual(soldier.experience, 50)

    def test_soldier_experience_negative(self):
        soldier = Soldier()
        soldier.experience = -400
        self.assertEqual(soldier.experience, 0)


    # @patch('builtins.print')
    # @patch('models.units.soldier.random')
    # def test_x(self, mock_random, p):
    #     soldier = Soldier()
        # mock_random.return_value = 6
        # soldier.random_value()
        # mock_random.return_value = 2
        # soldier.random_value()

        # mock_random.randint.side_effect = [1, 10, RuntimeError('da'), 20]
        # soldier.random_value()
        # soldier.random_value()
        # with self.assertRaises(RuntimeError):
        #     soldier.random_value()
        # soldier.random_value()
        # mock_random.randint.return_value = 1
        # soldier.random_value()
        # p.assert_called_once_with('y')
        # p.mock_calls

        # self.assertListEqual(p.mock_calls, [call('x')])
    # def test_is_value_less(self):
    #     soldier = Soldier()
    #     soldier.random_value()


if __name__ == '__main__':
    unittest.main()
