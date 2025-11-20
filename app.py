import os
import hydra
import logging
from omegaconf import DictConfig
from converter import Converter
from sheets import GSpreadClient, DataHandler
from normalizer import Normalizer
from validator import Validator

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

        # Initialize Normalizer and Validator
        normalizer = Normalizer()
        validator = Validator(cfg.openAI.model, cfg.openAI.token_limit, cfg.openAI.fine_tuning_cost_per_1000_tokens)

        # Extract and process data
        rows = data_handler.extract_data(gs.sheet_index)
        processed_data = []
        total_word_counts = 0
        total_token_counts = 0
        total_estimated_costs = 0

        for row in rows[1:]:
            prompt, completion = row[0], row[1]
            if prompt and completion:
                normalized_data = normalizer.normalize(prompt, completion)
                prompt = normalized_data["prompt"]
                completion = normalized_data["completion"]

                total_word_count, total_token_count, estimated_cost = validator.check_tokens(prompt, completion)

                total_word_counts += total_word_count
                total_token_counts += total_token_count
                total_estimated_costs += estimated_cost

                processed_data.append({"prompt": prompt, "completion": completion})

        # Print the output
        logger.info(f"Total word count: {total_word_counts}")
        logger.info(f"Estimated tokens: {total_token_counts}")
        logger.info(f"Estimated cost of fine-tuning: ${total_estimated_costs}\n")

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
