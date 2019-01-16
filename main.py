from models.battle import Battle
from models.battle import BattleTimer
import time


def main():
    timer = BattleTimer(100)

    print(timer.time)
    Battle("battle_config.json")


    print(timer.time)
    # new_army = Army(0, 3, 3)
    # print(new_army)
    # print("heeey")


if __name__ == '__main__':
    main()
