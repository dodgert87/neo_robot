from enum import Enum

class ErrorCode(Enum):
    INVALID_INPUT = 1001  # Input is empty or nonsensical
    UNKNOWN_QUERY = 1002  # Couldn't extract a valid command
    AI_PROCESSING_ERROR = 2001  # AI failed to generate a response
    JSON_PARSING_ERROR = 2002  # Failed to parse JSON from AI output
    EXTERNAL_API_ERROR = 3001 # Failed to fetch data from an external API (e.g., Weather API)
    UNSUPPORTED_LANGUAGE = 3002  # Language detected is not supported
    INTERNAL_ERROR = 5001  # Catch-all for unexpected failures
