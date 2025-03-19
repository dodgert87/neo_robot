from app.services.query_generators.query_service import QueryService
from app.services.ai_service import AIService
from app.core.error_codes import ErrorCode
from app.utils.json_utils import clean_and_parse_json
from app.utils.string_utils import clean_text

class ResponseService:
    """
    Handles AI-based processing of user queries.
    """

    @staticmethod
    def handle_request(cleaned_input: str, query_id: str, reference_query_id: str = None) -> dict:
        """
        Processes a cleaned user input by:
        1. Generating an AI extraction query.
        2. Calling AI to get structured JSON output.
        3. Formatting the final AI query.
        4. Calling AI to generate the final response.
        """

        ai_extraction_query = QueryService.query_request(cleaned_input)

        # Call AIService to get a raw string response
        ai_raw_response = AIService.call_ai_model(ai_extraction_query)
        #print(f"json struct{ai_raw_response}")

        # Clean and parse JSON externally
        extracted_json = clean_and_parse_json(ai_raw_response)
        #print(f"cleaned json struct{extracted_json}")


        if "error" in extracted_json and extracted_json["error"] == "Unsupported language detected":
            return {
                "queryId": query_id,
                "error": "Unsupported language detected",
                "language": extracted_json["language"],
                "error_code": ErrorCode.UNSUPPORTED_LANGUAGE.value
            }

        elif "error" in extracted_json:
            return {
                "queryId": query_id,
                "error": "AI failed to extract query details.",
                "error_code": ErrorCode.AI_PROCESSING_ERROR.value
            }

        # Attach queryId and referenceQueryId to extracted JSON
        extracted_json["queryId"] = query_id
        extracted_json["followUp"]["referenceQueryId"] = reference_query_id

        # Generate the final AI query using structured JSON
        ai_query = QueryService.generate_final_query(extracted_json)


        if "error" in ai_query:
            return {
                "queryId": query_id,
                "error": ai_query["error"],
                "error_code": ai_query["error_code"],
            }

        # Call AI Model again to get final response
        ai_response = AIService.call_ai_model(ai_query)

        # Handle AI failure in response generation
        if "error" in ai_response:
            return {
                "queryId": query_id,
                "error": ai_response,
                "error_code": ErrorCode.AI_PROCESSING_ERROR.value
            }


        return {
            "queryId": query_id,
            "command": extracted_json["command"],
            "tag": extracted_json["tag"],
            "parameters": extracted_json["parameters"],
            "response": clean_text(ai_response),
            "language_code": extracted_json["language"],
            "source": "AI",
            "cached": False,
            "followUp": {
                "status": extracted_json["followUp"]["status"],
                "referenceQueryId": reference_query_id
            }
        }