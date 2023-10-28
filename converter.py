import json
import os
from typing import List, Dict

# Convert data to JSONL format
class Converter:

    def to_jsonl(self, data: List[Dict[str, str]], filename: str) -> bool:
        try:
            # Get set directories
            current_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(current_dir, "Output")

            # Check if "output" folder exists, and create it if not
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Add "output/" before filename to save the file in the "output" folder
            filename_with_path = os.path.join(output_dir, filename)
            
            # Convert data to JSONL format
            with open(filename_with_path, "w") as f:
                for item in data:
                    json.dump(item, f)
                    f.write("\n")

            # Return True if successful
            return True
        
        # Raise exception if any error occurs
        except Exception as e:
            raise RuntimeError(f"Failed to convert data to JSONL format: {e}")
