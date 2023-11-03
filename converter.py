import json
import os
from typing import List, Dict

class Converter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir  

    def to_jsonl(self, data: List[Dict[str, str]], filename: str) -> bool:
        try:
            filename_with_path = os.path.join(self.output_dir, filename)
            
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
