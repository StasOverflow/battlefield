from battle_setup_set import ConfigSetup


if __name__ == '__main__':
    conf = ConfigSetup()
    setup = conf.default_unit_config('infantry', 'soldier')

    conf.setup_create(path_to_output_file='tests/test_soldier.json', setup=setup)

