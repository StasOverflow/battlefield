from battle_setup_set import ConfigSetup


if __name__ == '__main__':
    conf = ConfigSetup()
    setup = conf.army_config()

    conf.setup_create(path_to_output_file='tests/test_army.json', setup=setup)

