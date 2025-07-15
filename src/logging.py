import logging
logger = logging.getLogger("Jobs_Applier_Pro")
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(fmt)
if not logger.handlers:
    logger.addHandler(console)