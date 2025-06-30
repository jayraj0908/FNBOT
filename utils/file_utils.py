"""
Shared utility functions for file operations, date parsing, and common data processing tasks.
"""

import pandas as pd
import os
from datetime import datetime
from typing import Union, Optional, Dict, Any
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

def read_excel_file(file_input: Union[str, bytes], sheet_name=0, engine=None):
    """Reads an Excel file from a path or bytes into a pandas DataFrame."""
    try:
        if isinstance(file_input, str):
            if not os.path.exists(file_input):
                logger.error(f"File not found at path: {file_input}")
                raise FileNotFoundError(f"No such file or directory: '{file_input}'")
            logger.info(f"Reading Excel file from path: {file_input}")
            return pd.read_excel(file_input, sheet_name=sheet_name, engine=engine)
        elif isinstance(file_input, bytes):
            logger.info("Reading Excel file from bytes.")
            # Try calamine engine first, fallback to openpyxl if it fails
            try:
                return pd.read_excel(BytesIO(file_input), sheet_name=sheet_name, engine='calamine')
            except (ValueError, ImportError) as e:
                logger.warning(f"Calamine engine failed: {e}. Falling back to openpyxl.")
                return pd.read_excel(BytesIO(file_input), sheet_name=sheet_name, engine='openpyxl')
        else:
            raise TypeError("Input must be a file path (str) or bytes.")
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        raise

def read_csv_file(file_path: str, encoding: str = 'utf-8') -> pd.DataFrame:
    """
    Read CSV file with error handling and logging.
    
    Args:
        file_path: Path to the CSV file
        encoding: File encoding (default: utf-8)
        
    Returns:
        DataFrame from the CSV file
    """
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        logger.info(f"Successfully read CSV file: {file_path} with {len(df)} rows")
        return df
    except Exception as e:
        logger.error(f"Error reading CSV file {file_path}: {str(e)}")
        raise

def parse_date_column(df: pd.DataFrame, column_name: str, date_format: Optional[str] = None) -> pd.DataFrame:
    """
    Parse date column with flexible format detection.
    
    Args:
        df: DataFrame containing the date column
        column_name: Name of the column to parse
        date_format: Optional specific date format
        
    Returns:
        DataFrame with parsed date column
    """
    if column_name not in df.columns:
        logger.warning(f"Column {column_name} not found in DataFrame")
        return df
    
    try:
        if date_format:
            df[column_name] = pd.to_datetime(df[column_name], format=date_format, errors='coerce')
        else:
            df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
        
        # Log parsing results
        valid_dates = df[column_name].notna().sum()
        total_rows = len(df)
        logger.info(f"Parsed {valid_dates}/{total_rows} dates in column {column_name}")
        
    except Exception as e:
        logger.error(f"Error parsing date column {column_name}: {str(e)}")
    
    return df

def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names by removing extra spaces and converting to lowercase.
    
    Args:
        df: DataFrame to normalize
        
    Returns:
        DataFrame with normalized column names
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def save_excel_file(df: pd.DataFrame, file_path: str, sheet_name: str = 'Sheet1') -> str:
    """
    Save DataFrame to Excel file with error handling.
    
    Args:
        df: DataFrame to save
        file_path: Path where to save the file
        sheet_name: Name of the sheet (default: Sheet1)
        
    Returns:
        Path of the saved file
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save to Excel
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        logger.info(f"Successfully saved Excel file: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving Excel file {file_path}: {str(e)}")
        raise

def generate_output_filename(base_name: str) -> str:
    """
    Generate a unique output filename with timestamp.
    
    Args:
        base_name: Base name for the filename
        
    Returns:
        Generated filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.xlsx"

def validate_file_exists(file_path: str) -> bool:
    """
    Validate that a file exists and is readable.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if file exists and is readable, False otherwise
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    
    if not os.access(file_path, os.R_OK):
        logger.error(f"File not readable: {file_path}")
        return False
    
    return True

def cleanup_temp_files(file_paths: list) -> None:
    """
    Clean up temporary files with error handling.
    
    Args:
        file_paths: List of file paths to delete
    """
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Could not delete temporary file {file_path}: {str(e)}") 