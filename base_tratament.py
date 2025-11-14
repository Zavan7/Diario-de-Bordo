import os
import re
import logging
import pandas as pd
from config.logging_config import setup_logging

setup_logging()

class MailingProcessor:
    """
    Processes mailing data from an input Excel file, extracts relevant information,
    normalizes it, filters for Volkswagen-related entries, and saves the cleaned data
    to an output Excel file.
    """

    def __init__(self, input_file, output_file):
        """
        Initializes the MailingProcessor with input and output file paths.

        Args:
            input_file (str or Path): Path to the input Excel file containing raw mailing data.
            output_file (str or Path): Path where the processed data will be saved.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.regex = (
            r'(?P<campaign>\d+)\s*-\s*'
            r'(?P<institution>[A-Z\s]+?)\s*-\s*'
            r'(?P<ACD>\d+)\s*(?:-\s*)?'
            r'(?P<mailing>.+?)\s+'
            r'(?P<date>\d{2}/\d{2}/\d{4}\s*-\s*\d{2}:\d{2})'
            r'\s+Enviar mailing'
        )

    def load_input(self):
        try:
            df = pd.read_excel(self.input_file, header=None)
            df.columns = ['raw_text']
            logging.info(f"✅ Input file '{self.input_file}' loaded with {len(df)} lines.")
            return df
        except FileNotFoundError:
            logging.error(f"❌ Input file not found: {self.input_file}")
            raise
        except Exception as e:
            logging.error(f"❌ Error loading input file: {e}")
            raise

    def extract_data(self, df):
        try:
            valid_mask = df['raw_text'].str.match(self.regex)
            logging.info(f"Lines matching regex: {valid_mask.sum()} / {len(df)}")

            filtered_df = df[valid_mask]
            extracted = filtered_df['raw_text'].str.extract(self.regex)
            extracted = extracted.dropna().copy()

            # Ajuste de tipos para evitar float indesejado
            extracted['campaign'] = extracted['campaign'].astype(int)
            extracted['ACD'] = extracted['ACD'].astype(int)

            # Normaliza strings
            extracted['institution'] = extracted['institution'].str.strip().str.upper()
            extracted['mailing'] = extracted['mailing'].str.strip().str.upper()
            extracted['date'] = extracted['date'].str.strip()

            # Separa data e hora em colunas distintas
            extracted[['date_only', 'time_only']] = extracted['date'].str.split(r'\s*-\s*', expand=True)

            # Opcional: converter a data para datetime (útil pra ordenar ou validar)
            extracted['date_only'] = pd.to_datetime(extracted['date_only'], format='%d/%m/%Y', errors='coerce')

            logging.info(f"Lines extracted after regex and dropna: {len(extracted)}")

            # Retorna as colunas desejadas na ordem preferida
            return extracted[['campaign', 'institution', 'ACD', 'mailing', 'date_only', 'time_only']]

        except Exception as e:
            logging.error(f"❌ Error extracting data with regex: {e}")
            raise


        except Exception as e:
            logging.error(f"❌ Error extracting data with regex: {e}")
            raise

    def normalize(self, df):
        try:
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.strip().str.upper()
            logging.info("Data normalized (trim + upper).")
            return df
        except Exception as e:
            logging.error(f"❌ Error normalizing data: {e}")
            raise

    def load_existing(self):
        try:
            if os.path.exists(self.output_file):
                df_existing = pd.read_excel(self.output_file)
                df_existing = self.normalize(df_existing)
                logging.info(f"Existing file '{self.output_file}' loaded with {len(df_existing)} lines.")
                return df_existing
            else:
                logging.info(f"File '{self.output_file}' not found. Creating new.")
                return pd.DataFrame()
        except Exception as e:
            logging.error(f"❌ Error loading existing output file: {e}")
            raise

    def save_output(self, df):
        try:
            df.to_excel(self.output_file, index=False)
            logging.info(f"File '{self.output_file}' saved with {len(df)} lines.")
        except Exception as e:
            logging.error(f"❌ Error saving output file: {e}")
            raise

    def filter_volkswagen_only(self, df):
        try:
            filtered_df = df[df['institution'].str.contains('VOLKSWAGEN', na=False)]
            removed = len(df) - len(filtered_df)
            logging.info(f"Filtered out {removed} rows not containing 'VOLKSWAGEN' in 'institution' column.")
            return filtered_df
        except Exception as e:
            logging.error(f"❌ Error filtering only VOLKSWAGEN: {e}")
            raise

    def order(self, df, column):
        try:
            if column not in df.columns:
                raise ValueError(f"Column '{column}' not found in DataFrame.")
            df_sorted = df.sort_values(by=column, ascending=True)
            logging.info(f"📈 Data sorted by column '{column}'.")
            return df_sorted
        except Exception as e:
            logging.error(f"❌ Error sorting data by column '{column}': {e}")
            raise

    def process(self):
        try:
            input_df = self.load_input()
            new_data = self.extract_data(input_df)
            new_data = self.normalize(new_data)
            new_data = self.filter_volkswagen_only(new_data)
            new_data = new_data.drop_duplicates()

            existing_data = self.load_existing()

            if not existing_data.empty:
                combined = pd.concat([existing_data, new_data], ignore_index=True)
            else:
                combined = new_data

            # Removendo duplicatas por 'campaign' se fizer sentido no seu caso
            combined = combined.drop_duplicates(subset=['campaign'])

            combined = self.order(combined, column='campaign')

            self.save_output(combined)

            logging.info("✅ Processing finished. Unique records by campaign saved.")
            logging.info(f'\n As ultimas 10 linhas do arquivo, para confirmar antes de fazer backup \n')
            print(combined.tail(10))
            logging.info(f"📊 Total unique records: {len(combined)}")

        except Exception as e:
            logging.error(f"🚨 An error occurred during processing: {e}")
            raise
