import logging

# Create the logger and set its logging level to be debug
logger = logging.getLogger("Handy")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(levelname)s] [%(asctime)s] %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.propagate = False

logger.addHandler(console_handler)
