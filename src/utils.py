import logging
from pathlib import Path
import sys 
logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
    datefmt="%H:%M:%S"
    )
    if verbose is True:       
        logger.setLevel(logging.DEBUG) 
    elif verbose is False:
        logger.setLevel(logging.INFO)

def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if not Path(filepath).is_file():
        logger.error(f"Input file not found: '{filepath}'")  
        sys.exit(1)
        return False
    logger.info(f"Input file validated: {filepath}")
    return True


