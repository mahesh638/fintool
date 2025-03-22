import unittest
import os
from fintool_api import make_fintool_api_call

class TestFintoolAPI(unittest.TestCase):

    def test_make_fintool_api_call(self):
        """Test the actual API call without mocking"""
        company_ticker = "AAPL"
        financial_year = 2024

        # Ensure API credentials are set
        self.assertIsNotNone(os.getenv("FIN_TOOL_URL"), "FIN_TOOL_URL environment variable is missing.")
        self.assertIsNotNone(os.getenv("BEARER_TOKEN_FINTOOL_API"), "BEARER_TOKEN_FINTOOL_API environment variable is missing.")

        # Call the actual API
        response = make_fintool_api_call(company_ticker, financial_year)

        # Ensure response is not None
        self.assertIsNotNone(response, "API response should not be None.")
        
        # Unpack response
        current_year_risks, previous_year_risks = response

        # Ensure responses are strings
        self.assertIsInstance(current_year_risks, str, "Current year risks should be a string.")
        self.assertIsInstance(previous_year_risks, str, "Previous year risks should be a string.")

if __name__ == "__main__":
    unittest.main()
