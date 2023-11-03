# DatasetForge ⚒️

DatasetForge is a Python project designed to extract data from Google Sheets and convert it into JSONL formatted dataset, which is suitable for fine-tuning (`davinci-002` model) tasks (OpenAI). This tool also uses the library called [tiktoken](https://pypi.org/project/tiktoken/) to estimate the cost of fine-tuning (`davinci-002` model) tasks.

## Requirements ⭐

- You must have Google Sheets data that is represented in a prompt-completion (legacy) structure.
  > Refer to `sheets_sample.ods` for details
- You must [create a Google Service Account in Google Cloud Platform](https://www.howtogeek.com/devops/how-to-create-and-use-service-accounts-in-google-cloud-platform/).
- You must [enable the Google Sheets API for that Google Service Account](https://support.google.com/googleapi/answer/6158841?hl=en).
- You must have the credentials for that Google Service Account.


## How to Run the Project 🏃🏽‍♂️

**Step 1: Clone the repo**

Open Git bash and type:
```bash
  git clone https://github.com/farithadnan/DatasetForge.git
```

**Step 2: Installation** 

Install the required Python packages by running below command on your terminal:
  ```bash
    pip install -r requirements.txt
  ```

**Step 3: Set Up Google Sheets Config**

Ensure that the configuration file (e.g., `config.yaml`) contains essential settings such as:
- Path to Google Sheets credentials file (private keys).
- URL of the Google Sheet to extract data from.
- Index of the specific sheet within the Google Sheet.
- Name for the output JSONL file.
> Refer to a file called `config.yaml.sample` for more info.


**Step 4: Set up model for Encoding**

To estimate the cost of your dataset when it is fine-tuned later, you need to configure the encoding in `config.yaml`. By default, it is configured to `r50k_base` encoding, which refers to GPT-3 models like (`davinci-002`).
> For more details, refer to [How to count tokens with tiktoken](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb)

**Step 5: Run the Project**

Activate your virtual environment then run the main python script:

```bash
python app.py
```

This will authenticate with Google Sheets, extract the specified data, and convert it into a JSONL format, creating a dataset ready for fine-tuning tasks.

