import os
import hydra
import logging
from omegaconf import DictConfig
from converter import Converter
from extractor import GSpreadClient, DataHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@hydra.main(version_base=None, config_path="config", config_name="config.yaml")
def main(cfg: DictConfig):
    # Configure logging
    logger = logging.getLogger("main")

    try:        
        # Authenticate with Google Sheets
        logger.info("Authenticating with Google Sheets...")
        gs = cfg.gSheet
        client = GSpreadClient().Authenticate(gs.creds_path)

        # Extract data from Google Sheets
        logger.info("Extracting Data...\n")
        data_handler = DataHandler(cfg, client, gs.gs_url)
        processed_data = data_handler.extract_data(gs.sheet_index)

        # Convert data to JSONL format
        logger.info("Converting Data to JSONL Format...")

        # Get set directories
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(current_dir, "dataset")

        # Check if "output" folder exists, and create it if not
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        converter = Converter(output_dir)
        converter.to_jsonl(processed_data, cfg.output.filename)

        logger.info("Dataset for fine-tuning created successfully. Exiting...")
    except Exception as e:
        logger.exception(e)

# Call the main function
if __name__ == "__main__":
    main()
