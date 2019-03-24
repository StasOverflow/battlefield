import logging

LOG_FORMAT = '%(levelname)s %(time)s - %(unit)s, %(action)s'

logging.basicConfig(filename='battle.log',
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode='w')

battle_logger = logging.getLogger('logging.basicConfig')
