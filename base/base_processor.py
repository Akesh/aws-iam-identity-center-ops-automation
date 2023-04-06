import logging
import sys
LOGGER = logging.getLogger()


# LOGGER.setLevel(logging.INFO)
# HANDLER = logging.StreamHandler(sys.stdout)
# HANDLER.setLevel(logging.DEBUG)
# LOGGER.addHandler(HANDLER)


class BaseProcessor:

    def __init__(self):
        pass

    def raise_exception(self, msg):
        raise Exception(msg)

    def error_and_exit(self, error_msg='ERROR'):
        """Throw error and exit"""
        LOGGER.error(error_msg)
        sys.exit(1)

    def error_and_continue(self, error_msg='ERROR'):
        '''Throw error and contiune'''

        LOGGER.error(error_msg)
