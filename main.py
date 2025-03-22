import pandas as pd
import concurrent.futures
import json
import os
import time
from dotenv import load_dotenv
from fintool_api import make_fintool_api_call
from gpt_api import gpt_api_call
from utils import json_to_markdown

# Load environment variables
load_dotenv()

# Load the CSV file
file_path = "data/nasdaq-100.csv"
df = pd.read_csv(file_path)

# Function to handle API calls with exponential backoff
def call_with_retries(api_function, *args, max_retries=5):
    delay = 2  # Start with a 2-second delay
    for attempt in range(max_retries):
        result = api_function(*args)
        if result:
            return result  # Return if successful
        print(f"API call failed. Retrying in {delay} seconds... (Attempt {attempt+1}/{max_retries})")
        time.sleep(delay)
        delay *= 2  # Exponential backoff (2s → 4s → 8s → 16s)

    print(f"API call failed after {max_retries} attempts. Skipping...")
    return None  # Return None after max retries

# Main function to process all companies
def main():
    results = []

    # Using ThreadPoolExecutor with max_workers=5
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_company = {
            executor.submit(call_with_retries, make_fintool_api_call, row["ticker"], int(row["period"].replace("FY ", ""))): row
            for _, row in df.iterrows()
            if row["period"].replace("FY ", "").isdigit()
        }

        for future in concurrent.futures.as_completed(future_to_company):
            row = future_to_company[future]
            ticker = row["ticker"]
            fiscal_year = int(row["period"].replace("FY ", ""))

            try:
                current_year_risks, previous_year_risks = future.result()

                if current_year_risks and previous_year_risks:
                    print(f"Fintool API call successful for {ticker} FY{fiscal_year}")

                    gpt_response = call_with_retries(gpt_api_call, ticker, fiscal_year, current_year_risks, previous_year_risks)

                    # Convert GPT response from string to JSON
                    try:
                        gpt_response = json.loads(gpt_response)
                        gpt_response["company_ticket"] = ticker
                        results.append(gpt_response)
                        print(f"GPT API call successful for {ticker} FY{fiscal_year}")
                    except json.JSONDecodeError:
                        print(f"GPT response error for {ticker} FY{fiscal_year}: Invalid JSON format")

            except Exception as e:
                print(f"Error processing {ticker} FY{fiscal_year}: {e}")

    # Convert results to Markdown
    markdown_text = json_to_markdown(results)

    # Save Markdown to file
    with open("output_markup_files/nasdaq_100_risks.md", "w", encoding="utf-8") as f:
        f.write(markdown_text)

    print("Markdown file successfully generated: nasdaq_100_risks.md")

# Run the main function
if __name__ == "__main__":
    main()
