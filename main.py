from models.combat.battle import Battle
from models.combat.battle import BattleTimer


def main():
    config_file = '/models/combat/battle_setup.json'
    timer = BattleTimer(100)

    print(timer.time)
    battle = Battle(config_file)

    print(timer.time)
    # new_army = Army(0, 3, 3)
    # print(new_army)
    # print("heeey")


if __name__ == '__main__':
    main()
