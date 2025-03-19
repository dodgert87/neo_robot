import re

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing unnecessary formatting characters.

    - Removes newline (\n) and tab (\t) characters.
    - Replaces multiple spaces with a single space.
    - Trims leading and trailing spaces.

    :param text: The input string to clean.
    :return: A cleaned-up string.
    """
    if not isinstance(text, str):
        return ""

    # Remove newlines, tabs, and carriage returns
    text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # Trim leading and trailing spaces
    return text.strip()