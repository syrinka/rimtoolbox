import sys
from loguru import logger


logger.remove()
logger.add(sys.stderr, level=10)
logger.add('run.log', level=5)

# install
__builtins__['logger'] = logger