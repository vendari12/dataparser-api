from pandas import DataFrame
import csv
from typing import Tuple, List, Dict, Any
import pandas as pd
from django.http import HttpResponse


def normalize_data(df: DataFrame) -> DataFrame:
    """
    Normalizes the data to ensure consistent formatting across the DataFrame.
    This includes trimming whitespace, standardizing case, and converting date formats.

    Parameters:
        df (DataFrame): The input pandas DataFrame containing the CSV data.
    
    Returns:
        DataFrame: A normalized DataFrame with clean and consistent data.
    """
    # Strip leading/trailing spaces
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # Convert all text columns to lowercase for case-insensitive comparison
    df = df.map(lambda x: x.lower() if isinstance(x, str) else x)

    # Convert date columns to a consistent format (example: YYYY-MM-DD)
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]) or 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')

    return df


def reconcile(source_df: DataFrame, target_df: DataFrame) -> Tuple[DataFrame, DataFrame, List[Dict[str, Any]]]:
    """
    Reconciles the source and target DataFrames, identifying missing records and discrepancies.

    Parameters:
        source_df (DataFrame): The source data as a pandas DataFrame.
        target_df (DataFrame): The target data as a pandas DataFrame.
    
    Returns:
        Tuple[DataFrame, DataFrame, List[Dict[str, Any]]]: 
            - DataFrame: Records present in source but missing in target.
            - DataFrame: Records present in target but missing in source.
            - List[Dict]: List of discrepancies for records that exist in both files but differ in specific fields.
    """
    # Find records in source but not in target
    missing_in_target = source_df[~source_df.isin(target_df.to_dict(orient='list')).all(axis=1)]

    # Find records in target but not in source
    missing_in_source = target_df[~target_df.isin(source_df.to_dict(orient='list')).all(axis=1)]

    # Find discrepancies in matching records
    discrepancies = []
    common = pd.merge(source_df, target_df, how='inner', on=list(source_df.columns))
    for idx, row in common.iterrows():
        source_record = source_df[source_df == row]
        target_record = target_df[target_df == row]
        differences = (source_record != target_record)
        if differences.any(axis=None):
            discrepancies.append({
                "source_record": source_record.to_dict(),
                "target_record": target_record.to_dict(),
                "differences": differences.to_dict()
            })

    return missing_in_target, missing_in_source, discrepancies


def generate_csv_report(missing_in_target: DataFrame, missing_in_source: DataFrame, discrepancies: List[Dict[str, Any]]) -> HttpResponse:
    """
    Generates a CSV reconciliation report for download.

    Parameters:
        missing_in_target (DataFrame): DataFrame containing records missing in the target CSV.
        missing_in_source (DataFrame): DataFrame containing records missing in the source CSV.
        discrepancies (List[Dict]): A list of discrepancies between matching records in source and target.

    Returns:
        HttpResponse: A CSV file as an HTTP response, ready for download.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reconciliation_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Missing in Target'])
    writer.writerows(missing_in_target.values)

    writer.writerow([])
    writer.writerow(['Missing in Source'])
    writer.writerows(missing_in_source.values)

    writer.writerow([])
    writer.writerow(['Discrepancies'])
    for discrepancy in discrepancies:
        writer.writerow([discrepancy])

    return response
