from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()


class Risk(BaseModel):
    is_new_risk: bool
    risk: str

class Company(BaseModel):
    company_ticket: str
    fiscal_year: str
    risks: list[Risk]

# Define the API request function
def gpt_api_call(company_ticker, current_year, current_year_risks, previous_year_risks, model="gpt-4o-mini"):
    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")

    system_prompt = """You are a financial expert. You have the ability to understand financial risks in a company. Your task is to
    identify the new risks when you are given this year and last years risk sumarries from a companies 10K document"""

    prompt = (
        f"""For a given company, you are provided with the current and previous fiscal years' risks summarized as bullet points.
            Your task is to identify new risks. If any risk from the current year does not match any risk from the previous year, 
            mark it. Return only the risks for the current fiscal year in the following JSON format:"""

        f"""{{"
            "company_ticker" = {company_ticker},
            "fiscal_year": "FY{current_year}",
            "risks": [
                {{"is_new_risk": "True", "risk": "<current_year_risk_1>"}},
                {{"is_new_risk": "False", "risk": "<current_year_risk_2>"}}]
        }}"""

        f"""Each risk in the current year should be listed inside the "risks" list and compared against the previous year's risks.
            If it does not match any previous risk, mark "is_new_risk": "True". Otherwise, mark "is_new_risk": "False"."""

        f"""The risks for the current and previous years are:

        current_year_risks = The risks in the current year FY{current_year} are:
        {current_year_risks}

        previous_year_risks = The risks in the previous year FY{int(current_year) - 1} are:
        {previous_year_risks}

        Note: Your JSON output should not contain any references like [0000320193-23-000106_aapl-20230930.htm:37]. 
        Ensure that the entire risk description is included in the JSON output, not just the heading.
        """
    )


    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format=Company
        )
    except Exception as e:
        print(f"Error in GPT API: {e}")
        return None
    return response.choices[0].message.content


