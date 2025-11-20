import tiktoken
from typing import Tuple

class Validator:
    def __init__(self, model: str, token_limit: int, fine_tuning_cost_per_1000_tokens: float):
        self.model = model
        self.token_limit = token_limit
        self.fine_tuning_cost_per_1000_tokens = fine_tuning_cost_per_1000_tokens

    def check_tokens(self, prompt: str, completion: str) -> Tuple[int, int, float]:
        # Concatenate prompt and completion
        combined_text = prompt + " " + completion

        # Create a GPT-3 encoder instance
        encoder = tiktoken.get_encoding(self.model)

        # Calculate the number of tokens
        total_token_count = len(encoder.encode(combined_text))

        # Check if the total number of tokens has reached the limit
        if total_token_count > self.token_limit:
            raise ValueError("Error: The total number of tokens is greater than 2048.")

        # Calculate the estimated cost for fine-tuning
        estimated_cost = total_token_count * self.fine_tuning_cost_per_1000_tokens/1000
        total_word_count = len(combined_text.split())

        # Return Estimated Cost
        return total_word_count, total_token_count, estimated_cost
