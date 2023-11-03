import gspread
import tiktoken
import logging
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
        try:
            gc = gspread.service_account(filename=config_path)
            return gc
        except FileNotFoundError as e:
            raise RuntimeError(f"Failed to authenticate with Google Sheets due to missing credentials file: {e}")  
        except Exception as e:
            raise RuntimeError(f"Failed to authenticate with Google Sheets due to unexpected error: {e}")


class DataHandler:
    def __init__(self, cfg: DictConfig, gspread_client: gspread.client, google_sheet_url: str):
        self.openai_model = cfg.openAI.model
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

            processed_data = []
            total_word_counts = 0
            total_token_counts = 0
            total_estimated_costs = 0
            
            # Start from the second row, skip the headers
            for row in rows[1:]:
                prompt, completion = row[0], row[1]

                # TEMP - Check if both prompt and completion are not empty
                if prompt and completion:  
                    processed_data_item, total_word_count, total_token_count, estimated_cost = self.filter_data(prompt, completion)
                     
                     # Update the totals
                    total_word_counts += total_word_count
                    total_token_counts += total_token_count
                    total_estimated_costs += estimated_cost

                    # Append the processed data
                    processed_data.extend(processed_data_item)
                
            # Print the output
            logger.info(f"Total word count: {total_word_counts}")
            logger.info(f"Estimated tokens: {total_token_counts}")
            logger.info(f"Estimated cost of fine-tuning: ${total_estimated_costs}\n")

            # Return the processed data
            return processed_data
        
        except (AttributeError, KeyError) as e:
            print(f"An AttributeError or KeyError occurred: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to extract data from Google Sheets: {e}")


    def filter_data(self, prompt: str, completion: str) -> List[Dict[str, str]]:
        filtered_data = []
        try:
            # Remove leading & trailing whitepace in the left & the right
            prompt = prompt.lstrip().rstrip()
            completion = completion.lstrip().rstrip()

            # Check and add "\n\n###\n\n" at the end of prompt
            if not prompt.endswith("\n\n###\n\n"):
                prompt += " \n\n###\n\n"
            
            # Check and add "." at the end of completion
            if not completion.endswith("."):
                completion += "."

            # Check and add "END" at the end of completion
            if not completion.endswith("END"):
                completion += " END"
            
            ## Check and add " " at the front of completion
            if not completion.startswith(" "):
                completion = " " + completion
            
            # Check tokens validity
            total_word_count, total_token_count, estimated_cost = self.check_tokens(prompt, completion)

            # Append the processed data
            filtered_data.append({"prompt": prompt, "completion": completion})

            # Return the processed data
            return filtered_data, total_word_count, total_token_count, estimated_cost
        
        except (AttributeError, KeyError) as e:
            print(f"An AttributeError or KeyError occurred: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to extract data from Google Sheets: {e}")


    def check_tokens(self, prompt: str, completion: str):
        '''
        Method to check the number of tokens

        Args:
            prompt: The prompt text
            completion: The completion text
        
        Returns:
            The total number of words, the total number of tokens, and the estimated cost
        '''
        try:
            # Concatenate prompt and completion
            combined_text = prompt + " " + completion

            # Create a GPT-3 encoder instance
            encoder = tiktoken.get_encoding(self.openai_model)

            # Calculate the number of tokens
            total_token_count = len(encoder.encode(combined_text))

            # Check if the total number of tokens has reached the limit
            if total_token_count > 2048:
                raise ValueError("Error: The total number of tokens is greater than 2048.")
            
            # Calculate the estimated cost for fine-tuning
            estimated_cost = total_token_count * 0.0300/1000
            total_word_count = len(combined_text.split())

            # Return Estimated Cost
            return total_word_count, total_token_count, estimated_cost
            
        except Exception as e:
            raise RuntimeError(f"Failed to check tokens: {e}")
