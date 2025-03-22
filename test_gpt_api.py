import unittest
import json  # Import JSON module
from gpt_api import gpt_api_call

class TestGPTAPI(unittest.TestCase):

    def test_get_api_call(self):
        company_ticker = "APPL" 
        current_year = "2024"
        current_year_risks = """The risks faced by Apple Inc. in FY2024, as outlined in its 10-K filing, include:

1. **Macroeconomic Conditions**: Inflation, interest rates, and currency fluctuations directly and indirectly impacted the company’s operations and financial condition, with potential for future material effects.

2. **Foreign Exchange Rate Risk**: Strengthening of the U.S. dollar negatively affected net sales and gross margins expressed in U.S. dollars, and fluctuations in exchange rates impacted the fair values of certain assets and liabilities.

3. **Interest Rate Risk**: Rising interest rates could reduce the fair value of the company’s investment portfolio and increase interest expenses on term debt.

4. **Legal and Regulatory Risks**: The company faced uncertainties related to legal proceedings, claims, and tax positions, including intercompany transfer pricing and deemed repatriation tax, which could materially impact financial results.

5. **Volatility in Gross Margins**: Future gross margins were expected to face volatility and downward pressure due to various factors, including product mix, cost savings, and foreign currency weaknesses."""

        previous_year_risks = """Here are five key risks mentioned in Apple's FY2023 10-K filing:

- **Macroeconomic Conditions**: Inflation, changes in interest rates, and currency fluctuations have impacted and could continue to materially impact Apple's results of operations and financial condition.

- **Foreign Exchange Rate Risk**: As a net receiver of currencies other than the U.S. dollar, changes in exchange rates, especially a strengthening U.S. dollar, could negatively affect Apple's net sales and gross margins.

- **Interest Rate Risk**: Fluctuations in U.S. interest rates could negatively affect the fair value of Apple's investment portfolio and increase interest expenses on term debt.

- **Volatility in Gross Margins**: Apple's gross margins are subject to volatility and downward pressure due to various factors, including foreign currency weakness and changes in product and service mix.

- **Operational Risks**: Risks related to the design or operation of internal controls over financial reporting could adversely affect Apple's ability to record, process, summarize, and report financial information accurately."""

        # Call the GPT API function
        gpt_return = gpt_api_call(company_ticker, current_year, current_year_risks, previous_year_risks)

        # Ensure the API response is not None
        self.assertIsNotNone(gpt_return, "API response should not be None.")

        # Convert JSON string to dictionary
        try:
            gpt_return = json.loads(gpt_return)  # Deserialize JSON string to dictionary
        except json.JSONDecodeError as e:
            self.fail(f"Failed to parse JSON response: {e}")

        # Assertions to validate the structure of the response
        self.assertIsInstance(gpt_return, dict, "Response should be a dictionary.")
        self.assertIn("risks", gpt_return, "Response should contain a 'risks' key.")
        self.assertIsInstance(gpt_return["risks"], list, "'risks' should be a list.")

        # Check that each risk item has the expected keys
        for risk in gpt_return["risks"]:
            self.assertIsInstance(risk, dict, "Each risk should be a dictionary.")
            self.assertIn("risk", risk, "Each risk should have a 'risk' key.")
            self.assertIn("is_new_risk", risk, "Each risk should have an 'is_new_risk' field.")
            self.assertIsInstance(risk["risk"], str, "'risk' should be a string.")
            self.assertIsInstance(risk["is_new_risk"], bool, "'is_new_risk' should be a boolean.")

if __name__ == "__main__":
    unittest.main()
