from models.combat.battle import Battle


def main():
    config_file = 'combat_setup.json'

    battle = Battle(config_file)

    while not battle.winner_get():
        battle.clockwise_attack()
        battle.battle_log_schedule(3)


if __name__ == '__main__':
    main()
