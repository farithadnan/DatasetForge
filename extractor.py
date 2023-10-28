import gspread
import tiktoken
from typing import List, Dict

# Class that handles the authentication with Google Sheets
class GSpreadClient:
    # Constructor
    def __init__(self, config_path: str):
        self.config_path = config_path

    # Method to authenticate with Google Sheets
    def Authenticate(self):
        try:
            # Authenticate with Google Sheets
            gc = gspread.service_account(filename=self.config_path)

            # Return the authenticated client
            return gc
        
        # Raise exception if any error occurs
        except Exception as e:
            raise RuntimeError(f"Failed to authenticate with Google Sheets: {e}")


# Class to extract data from Google Sheets
class DataHandler:
    # Constructor
    def __init__(self, gspread_client: gspread.client, google_sheet_url: str):
        self.gspread_client = gspread_client
        self.google_sheet_url = google_sheet_url

    # Method to extract data from Google Sheets
    def extract_data(self, sheet_index: int) -> List[Dict[str, str]]:
        try:
            # Extract data from Google Sheets
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
            print(f"\nTotal word count: {total_word_counts}")
            print(f"Estimated tokens: {total_token_counts}")
            print(f"Estimated cost of fine-tuning: ${total_estimated_costs}\n")

            # Return the processed data
            return processed_data
        
        # Raise exception if any error occurs
        except Exception as e:
            raise RuntimeError(f"Failed to extract data from Google Sheets: {e}")


    # Method to process the data
    def filter_data(self, prompt: str, completion: str) -> List[Dict[str, str]]:
        filtered_data = []

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


    # Method to check tokens
    def check_tokens(self, prompt: str, completion: str):
        try:
            # Concatenate prompt and completion
            combined_text = prompt + " " + completion

            # Create a GPT-3 encoder instance
            encoder = tiktoken.get_encoding("r50k_base")

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
