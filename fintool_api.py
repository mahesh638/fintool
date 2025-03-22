import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Define the API URL
def make_fintool_api_call(company_ticker, financial_year):
    url = os.getenv('FIN_TOOL_URL')
    token = os.getenv('BEARER_TOKEN_FINTOOL_API')

    # Define the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",  # Replace <token> with the actual token
        "X-LLM-Priority": "low"
    }

    # Define the request payload
    query = f"""What were the key risks in FY{str(financial_year)} based on the 10-K SEC filing? 
    Provide five bullet points, with each containing up to three sentences. Focus on the most significant risks."""
    payload = {
        "tickers": [company_ticker],  
        "publication_ids": [],
        "messages": [{"role": "user", "content": query}],  
        "use_caching": False,
        "search_result_ids": [],
        "stream": False,
        "skip_company_screener": True,
        "skip_spreadsheet_builder": True
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Print the response
    if response.status_code == 200:
        try:
            data = response.json()
            current_year_risks = data["content"]
        except requests.exceptions.JSONDecodeError:
            print("Error in Fintool API: Unable to decode JSON response in Fintool API call")
            return None
    else:
        print(f"Error in Fintool API: Received status code {response.status_code}")
        return None

    second_query = f"What were the risks in the FY{str(financial_year -1)} according to the 10K SEC filing? Answer in 5 bullet points."
    payload["messages"] = [{"role": "user", "content": second_query}]
    
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            data = response.json()
            previous_year_risks = data["content"]
        except requests.exceptions.JSONDecodeError:
            print("Error in Fintool API: Unable to decode JSON response")
            return None
    else:
        print(f"Error in Fintool API: Received status code {response.status_code}")
        return None

    return current_year_risks, previous_year_risks
    



# print(make_fintool_api_call("APPL", 2023))