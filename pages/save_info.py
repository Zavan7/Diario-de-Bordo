import logging
import tempfile
import pandas as pd
from pathlib import Path
from config.logging_config import setup_logging

setup_logging()

def append_mailing(self, mailing_list):
    """
    Appends new mailing data to an existing Excel file, or creates the file if it doesn't exist.

    This method processes a list of strings, splits each string by newline characters, and appends
    the resulting lines to an Excel file specified by `self.file_path`.

    Steps:
        - Flatten all lines from the input list `mailing_list`.
        - Create a DataFrame from the collected lines.
        - If the Excel file exists, load it and concatenate it with the new data.
        - If not, use only the new data.
        - Save the combined data to a temporary Excel file and replace the original file atomically.
        - Log the number of new lines added and the destination file path.

    Notes:
        - `self.file_path` must be a valid `Path` object pointing to the Excel file location.

    Args:
        mailing_list (list): A list of strings, each possibly containing multiple lines of mailing data.
    """
    
    all_lines = []
    for item in mailing_list:
        all_lines.extend(item.split('\n'))

    df_new = pd.DataFrame(all_lines, columns=['raw_text'])

    if self.file_path.exists():
        df_existing = pd.read_excel(self.file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        temp_path = tmp.name
    df_combined.to_excel(temp_path, index=False)
    Path(temp_path).replace(self.file_path)
    logging.info(f"✅ {len(df_new)} lines added to the file '{self.file_path}'.")