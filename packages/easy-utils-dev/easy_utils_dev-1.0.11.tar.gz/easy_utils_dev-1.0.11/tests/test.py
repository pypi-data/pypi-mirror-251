from easy_utils_dev.simple_sqlite import *
from easy_utils_dev.debugger import DEBUGGER


def test( message=None ) :
    print(f"s : {message}")

logger = DEBUGGER('db-connector')
logger.wrappLogger( lambda: test( 'test'))

logger.info('ss')