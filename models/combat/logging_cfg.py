import logging

LOG_FORMAT = '%(levelname)s %(asctime)-12s - %(message)s'

logging.basicConfig(filename='battle.log',
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode='w')

battle_logger = logging.getLogger('logging.basicConfig')
battle_logger.addHandler(logging.StreamHandler())
