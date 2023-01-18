import sys
from loguru import logger


logger.remove()
logger.add(sys.stderr, level=10)
# flush log every time
# shall be configurable later
logger.add(
    open('run.log', 'w', encoding='utf-8'),
    level=5
)

# install
__builtins__['logger'] = logger