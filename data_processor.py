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
    if axis != "rows" or axis != "columns":
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError
    rows_removed = df.dropna()
    columns_dropped = df.dropna(axis=1)
    logger.debug(f"Rows removed: {rows_removed}, Columns removed: {columns_dropped}")
    return df

def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method == "iqr" or method == "zscore":
        q1 = df[columns].quantile(0.25)
        q3 = df[columns].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr
        mean = df[columns].mean()
        std = df[columns].std()
        z_scores = (df["Score"] - mean) / std
    else:
        logger.error("Method does not exist")
        raise ValueError
    before = len(df)
    if columns not in df.columns.tolist():
        logger.warning("A configured column does not exist")
    if columns is not pd.api.types.is_any_real_numeric_dtype(df[columns]):
        logger.warning("A configured column is not numeric")
    else:
        if method == 'iqr':
            df = df[(df[columns] >= lower) & (df[columns] <= upper)]
        else:
            df = df[z_scores.abs() <= 3]
    logger.debug(f"Method: {method}, Threshold: {threshold}, Rows removed: {before - df}")
    df

def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    remove_duplicates(df)
    handle_missing(df, axis=config)
    remove_outliers(df, config, config, config)
    return df

def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {'rows_before': df_before.shape[0], 'rows_after': df_after.shape[0], 'rows_removed': df_before.shape[0] - df_after.shape[0], 'columns_before': df_before.shape[1], 'columns_after': df_after.shape[1], 'columns_removed': df_before[1] - df_after[1]}
