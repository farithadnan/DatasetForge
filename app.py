import logging
from logging import config
import os
from converter import Converter
from dotenv import dotenv_values
from extractor import GSpreadClient, DataHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Class to manage the config file
class ConfigManager:

    # Constructor
    def __init__(self, config_path):
        self.config_path = config_path

    # Method to get the gSheet config from the .env file
    def load_config(self):

        # Get the config from the .env file
        config = dotenv_values(self.config_path)
        google_sheet_keys_path = config["GS_CONFIG_PATH"]
        google_sheet_url = config["GSPREAD_URL"]
        sheet_index = int(config["SHEET_INDEX"])
        filename = config["FILENAME"]

        # Check if the config is valid
        if not google_sheet_keys_path or not google_sheet_url:
            print("Error: GS_CONFIG_PATH and GSPREAD_URL must be provided in the .env file.")
            return None

        # Return the config details
        return google_sheet_keys_path, google_sheet_url, sheet_index, filename

# Main function
def main():
    # Configure logging
    logger = logging.getLogger("main")

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the gSheet config from the .env file
    config_path = os.path.join(current_dir, "Secrets", ".env")
    logger.info("Fetch Configuration Details...")
    gspread_config = ConfigManager(config_path).load_config()
    
    # Check if the config is valid
    if not gspread_config:
        logger.error("Invalid gspread configuration. Exiting...")
        return
    
    # Assign the config details
    google_sheet_keys_path, google_sheet_url, sheet_index, filename = gspread_config
    
    # Authenticate with Google Sheets
    logger.info("Authenticating with Google Sheets...")
    client = GSpreadClient(google_sheet_keys_path).Authenticate()

    # Extract data from Google Sheets
    logger.info("Extracting Data...")
    data_handler = DataHandler(client, google_sheet_url)
    processed_data = data_handler.extract_data(sheet_index)

    # Convert data to JSONL format
    logger.info("Converting Data to JSONL Format...")
    converter = Converter()
    converter.to_jsonl(processed_data, filename)

    logger.info("Dataset for fine-tuning created successfully. Exiting...")

# Call the main function
if __name__ == "__main__":
    main()
