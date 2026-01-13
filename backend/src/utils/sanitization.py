import re
from typing import Union

def sanitize_input(input_data: Union[str, None]) -> Union[str, None]:
    """
    Sanitize user input to prevent XSS and other injection attacks.

    Args:
        input_data: String input to sanitize

    Returns:
        Sanitized string or None if input is None
    """
    if input_data is None:
        return None

    # Remove potentially dangerous characters/sequences
    sanitized = input_data

    # Remove script tags (case insensitive)
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)

    # Remove javascript: hrefs
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)

    # Remove data: hrefs
    sanitized = re.sub(r'data:', '', sanitized, flags=re.IGNORECASE)

    # Remove event handlers (onload, onclick, etc.)
    sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)

    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()

    return sanitized

def sanitize_email(email: str) -> str:
    """
    Sanitize email input specifically.

    Args:
        email: Email string to sanitize

    Returns:
        Sanitized email string
    """
    if not email:
        return email

    # Basic email sanitization
    sanitized = email.strip().lower()

    # Additional validation could be added here
    return sanitized

def sanitize_title(title: str) -> str:
    """
    Sanitize task title input.

    Args:
        title: Title string to sanitize

    Returns:
        Sanitized title string
    """
    if not title:
        return title

    # Sanitize the input
    sanitized = sanitize_input(title)

    # Additional title-specific sanitization could be added
    return sanitized

def sanitize_description(description: str) -> str:
    """
    Sanitize task description input.

    Args:
        description: Description string to sanitize

    Returns:
        Sanitized description string
    """
    if not description:
        return description

    # Sanitize the input
    sanitized = sanitize_input(description)

    return sanitized