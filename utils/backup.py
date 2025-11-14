import pandas as pd
import os
import logging
from config.logging_config import setup_logging

setup_logging()

class BackupGenerator:
    """
    Handles backup creation and updating by merging new data files into a master backup file,
    removing duplicates based on a unique column.
    """

    def __init__(self, backup_dir='backups'):
        """
        Initialize BackupGenerator with a directory to store backups.

        Parameters:
        backup_dir (str): Directory path where backups will be stored.
        """
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def generate_backup(self, file_path: str, unique_column: str = 'campaign') -> str:
        """
        Generate or update a backup Excel file by merging new data with existing backup,
        removing duplicates based on a unique column.

        Parameters:
        file_path (str): Path to the new data file (Excel or CSV).
        unique_column (str): Column name used to identify duplicates.

        Returns:
        str: Path to the updated backup Excel file.

        Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the file format is unsupported or unique_column is missing.
        Exception: For other unexpected errors during backup generation.
        """
        try:
            if not os.path.isfile(file_path):
                msg = f"File '{file_path}' not found."
                logging.error(msg)
                raise FileNotFoundError(msg)

            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.xls', '.xlsx']:
                df_new = pd.read_excel(file_path)
            elif ext == '.csv':
                df_new = pd.read_csv(file_path)
            else:
                msg = f"Unsupported file format '{ext}'."
                logging.error(msg)
                raise ValueError(msg)

            if unique_column not in df_new.columns:
                msg = f"Column '{unique_column}' not found in the file."
                logging.error(msg)
                raise ValueError(msg)

            backup_path = os.path.join(self.backup_dir, 'backup_new.xlsx')

            if os.path.isfile(backup_path):
                df_backup = pd.read_excel(backup_path)
                df_combined = pd.concat([df_backup, df_new], ignore_index=True)
            else:
                df_combined = df_new

            original_count = len(df_combined)
            df_unique = df_combined.drop_duplicates(subset=unique_column)
            unique_count = len(df_unique)

            df_unique.to_excel(backup_path, index=False)

            logging.info(
                f"Backup updated: {backup_path} | Records: {original_count} → {unique_count}"
            )

            return backup_path

        except Exception as e:
            logging.exception(f"Error generating backup: {e}")
            raise