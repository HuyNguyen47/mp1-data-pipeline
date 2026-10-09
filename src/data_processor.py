# data_processor.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    before = df.copy()
    df = df.drop_duplicates()    
    logger.debug(f"# of Rows before remove: {len(before)}, # of Rows after remove: {len(df)}")
    return df

def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis not in ["rows", "columns"]:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError
    rows_removed = df.dropna()
    columns_dropped = df.dropna(axis=1)
    logger.debug(f"Rows removed: {len(rows_removed)}, Columns removed: {len(columns_dropped)}")
    return df

def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method in ["iqr", "zscore"]:
        before = len(df)
        missing_columns = [col for col in columns if col not in df.columns]
        if missing_columns:
            logger.warning("A configured column does not exist")
        if pd.api.types.is_numeric_dtype(columns) == True:
            q1 = df[columns].quantile(0.25)
            q3 = df[columns].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
            mean = df[columns].mean()
            std = df[columns].std()
            z_scores = (df[columns] - mean) / std
            if method == 'iqr':
                df = df[(df[columns] >= lower) & (df[columns] <= upper)]
            else:
                df = df[z_scores.abs() <= 3]
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]) == False:
                logger.warning("A configured column is not numeric")
        logger.debug(f"Method: {method}, Threshold: {threshold}, Rows removed: {before - len(df)}")
        return df
    else:
        logger.error("Method does not exist")
        raise ValueError
    
 

def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    #check if removing duplic is enabled, if so then we run remov..()
    if config["processing"]["remove_duplicates"]:
        df = remove_duplicates(df)
    if config["processing"]["missing"]["enabled"]:
        df = handle_missing(df, axis=config["processing"]["missing"]["axis"])
    if config["processing"]["outliers"]["enabled"]:
        df = remove_outliers(df, columns=config["processing"]["outliers"]["columns"], method=config["processing"]["outliers"]["method"], threshold=config["processing"]["outliers"]["threshold"])
    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {'rows_before': df_before.shape[0], 'rows_after': df_after.shape[0], 'rows_removed': df_before.shape[0] - df_after.shape[0], 'columns_before': df_before.shape[1], 'columns_after': df_after.shape[1], 'columns_removed': df_before.shape[1] - df_after.shape[1]}

