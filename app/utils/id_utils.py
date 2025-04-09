from datetime import datetime, timezone
import uuid

UNKNOWN_USER_PREFIX = "unknown"

def generate_chat_id(user_id: str) -> str:
    """
    Generates a unique chat ID in the format: user_id_dd-mm-yyyy
    This allows session management per user per day.
    """
    date_str = datetime.now(timezone.utc).strftime("%d-%m-%Y")
    return f"{user_id}_{date_str}"

def generate_fallback_user_id() -> str:
    """
    Generates a fallback user ID for users without a defined user ID.
    Format: unknown_<UUID4>
    """
    return f"{UNKNOWN_USER_PREFIX}_{uuid.uuid4().hex}"
