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
from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)



logger = logging.getLogger(__name__)



def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Parsing command-line arguments")
    parser.add_argument(
                    "--input",
                    "-i",
                    required=True, 
                    help="Path to the input file")
    parser.add_argument(
                    "--config",
                    required=True, 
                    help="Path to a YAML configuration file")

    parser.add_argument("--output", 
                    "-o",
                    required=True,
                    help="Path to the output file")

    parser.add_argument("--verbose", 
                    "-v", 
                    action="store_true",
                    help="Enable verbose logging")
    return parser.parse_args()



def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(f"Arguments parsed: input={args.input}, output={args.output}")
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)
    try:
        data = load_data(args.input)
        data_config = load_data(args.config)
    except ValueError:
        sys.exit(1)
    
    data_original = data.copy()
    try:
        validated_df = validate_dataframe(data, data_config["validation"]["required_columns"], data_config["validation"]["numeric_columns"])
    except:
        sys.exit(1)
    logger.info(f"Number of rows before validation: {len(data_original)}, Number of rows after validation: {len(validated_df)}")

    try:
        cleaned_data = process_data(validated_df, data_config)
    except ValueError:
        sys.exit(1)
    data_new = cleaned_data.copy()
    
    logger.info(f"Processing complete: {len(data_original)} -> {len(data_new)}")
    save_data(cleaned_data, args.output)
    logger.info(f"Saved cleaned data to {args.output}")
    print(create_cleaning_report(data_original, data_new))

    

if __name__ == "__main__":

    main()
