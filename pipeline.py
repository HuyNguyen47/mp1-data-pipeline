# Starter Code
## `pipeline.py`

"""
Data Processing Pipeline - CLI Template
DS 3500 - MP1
Usage:
python pipeline.py --input data.csv --output clean.csv
python pipeline.py --input data.csv --output results.json --format json --
verbose
"""
import argparse
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
    )
    if verbose is True:       
        logger.setLevel(logging.DEBUG) 
    elif verbose is False:
        logger.setLevel(logging.INFO)
    

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Parsing command-line arguments")
    parser.add_argument(
                    "--input",
                    "-i",
                    required=True, 
                    help="Path to the input file")

    parser.add_argument("--output", 
                    "-o",
                    required=True,
                    help="Path to the output file")
    
    parser.add_argument("--format", 
                    default=".csv",
                    help="Output format: 'csv' or 'json'; default is csv")

    parser.add_argument("--verbose", 
                    "-v", 
                    action="store_true",
                    help="Enable verbose logging")
    return parser.parse_args()

def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if not Path(filepath.input).is_file():
        logger.error(f"Input file not found: '{filepath.input}'")  
        sys.exit(1)
        return False
    logger.debug(f"Arguments parsed: input={filepath.input}, output={filepath.output}")
    logger.info(f"Input file validated: '{filepath.input}'")
    return True

def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    validate_input(args)


if __name__ == "__main__":
    main()
