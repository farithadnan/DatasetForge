import gspread
import tiktoken
import logging
import os
from omegaconf import DictConfig
from typing import List, Dict

class GSpreadClient:
    def __init__(self):
        pass

    def Authenticate(self, config_path: str):
        '''
        Method to authenticate with Google Sheets

        Returns:
            The authenticated Google Sheets client
        '''
        self.validate_credentials(config_path)
        try:
            gc = gspread.service_account(filename=config_path)
            return gc
        except Exception as e:
            raise RuntimeError(f"Failed to authenticate with Google Sheets: {e}")

    def validate_credentials(self, config_path: str):
        '''
        Method to validate the Google Sheets credentials

        Args:
            config_path: The path to the credentials file
        '''
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"The credentials file was not found at {config_path}")


class DataHandler:
    def __init__(self, cfg: DictConfig, gspread_client: gspread.client, google_sheet_url: str):
        self.openai_model = cfg.openAI.model
        self.token_limit = cfg.openAI.token_limit
        self.fine_tuning_cost_per_1000_tokens = cfg.openAI.fine_tuning_cost_per_1000_tokens
        self.gspread_client = gspread_client
        self.google_sheet_url = google_sheet_url

    def extract_data(self, sheet_index: int) -> List[Dict[str, str]]:
        '''
        Method to extract data from Google Sheets

        Args:
            sheet_index: The index of the sheet to extract data from

        Returns:
            The extracted data
        '''
        logger = logging.getLogger("DataHandler")
        try:
            sh = self.gspread_client.open_by_url(self.google_sheet_url)
            worksheet = sh.get_worksheet(sheet_index)
            rows = worksheet.get_all_values()
            return rows
        except Exception as e:
            raise RuntimeError(f"Failed to extract data from Google Sheets: {e}")
