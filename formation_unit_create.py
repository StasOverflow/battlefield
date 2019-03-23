from battle_setup_set import ConfigSetup


if __name__ == '__main__':
    conf = ConfigSetup()
    setup = conf.random_squad_config()

    conf.setup_create(path_to_output_file='tests/test_squad.json', setup=setup)

