import json
import re
from app.core.error_codes import ErrorCode

def clean_json_string(json_str: str) -> str:
    """
    Cleans the JSON string by removing unwanted characters.
    """
    cleaned_str = re.sub(r'\s+', ' ', json_str)  # Remove excessive whitespace
    return cleaned_str

def clean_and_parse_json(raw_str: str) -> dict:
    """
    Cleans raw string returned by AI and parses it into JSON.
    - Removes non-JSON characters (before and after JSON body).
    - Returns parsed JSON or an error with error code.
    """

    # Attempt to isolate JSON object using regex
    json_match = re.search(r"\{.*\}", raw_str, re.DOTALL)

    if not json_match:
        return {
            "error": "No valid JSON structure found in the AI response.",
            "error_code": ErrorCode.JSON_PARSING_ERROR.value
        }

    cleaned_str = json_match.group(0)

    try:
        parsed_json = json.loads(clean_json_string(cleaned_str))
        return parsed_json
    except json.JSONDecodeError as e:
        return {
            "error": f"JSON parsing error: {str(e)}",
            "error_code": ErrorCode.JSON_PARSING_ERROR.value
        }