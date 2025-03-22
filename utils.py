import json

def json_to_markdown(risk_data_list):
    """
    Converts a list of JSON risk summaries into a formatted Markdown table.
    
    Args:
        risk_data_list (list): List of JSON objects containing company risks.

    Returns:
        str: A Markdown-formatted string.
    """

    markdown_output = "# NASDAQ-100 Risk Summary\n\n"
    markdown_output += "| Index | Company Ticket | Fiscal Year | Risks (Bullet Points) | New Risks Highlighted |\n"
    markdown_output += "|-------|---------------|-------------|-----------------------|----------------------|\n"

    index = 1
    for risk_data in risk_data_list:
        company = risk_data["company_ticket"]
        financial_year = risk_data["fiscal_year"]

        # Format risks as bullet points within a single cell
        risks_formatted = ""
        new_risks_formatted = ""
        
        for risk_entry in risk_data["risks"]:
            risk_text = risk_entry["risk"]
            is_new = "**Yes**" if risk_entry["is_new_risk"] else "No"
            
            risks_formatted += f"- {risk_text}\n"
            new_risks_formatted += f"- {is_new}\n"

        # Replace newline characters with <br> for proper Markdown formatting
        risks_formatted = risks_formatted.strip().replace("\n", "<br>")
        new_risks_formatted = new_risks_formatted.strip().replace("\n", "<br>")

        markdown_output += f"| {index} | {company} | {financial_year} | {risks_formatted} | {new_risks_formatted} |\n"
        index += 1  # Increment index per company-year group

    return markdown_output
