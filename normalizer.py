from typing import Dict

class Normalizer:
    def normalize(self, prompt: str, completion: str) -> Dict[str, str]:
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

        return {"prompt": prompt, "completion": completion}
