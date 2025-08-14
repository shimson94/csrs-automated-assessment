"""
Helper utility functions for the CSRS Automated Assessment System
"""

from datetime import datetime, timezone
from typing import Optional


def format_datetime(dt: Optional[datetime], format_string: str = "%Y-%m-%d %H:%M:%S") -> Optional[str]:
    """
    Format a datetime object to string
    
    Args:
        dt: The datetime to format
        format_string: The format string to use
        
    Returns:
        str: Formatted datetime string or None if dt is None
    """
    if dt is None:
        return None
    return dt.strftime(format_string)


def calculate_late_penalty(due_date: datetime, submission_date: datetime, penalty_per_day: float = 0.1) -> tuple[bool, int, float]:
    """
    Calculate late submission penalty
    
    Args:
        due_date: The assignment due date
        submission_date: The actual submission date
        penalty_per_day: Penalty percentage per day late (default 10%)
        
    Returns:
        tuple: (is_late, days_late, penalty_multiplier)
    """
    if submission_date <= due_date:
        return False, 0, 1.0
    
    # Calculate days late
    time_diff = submission_date - due_date
    days_late = time_diff.days + (1 if time_diff.seconds > 0 else 0)  # Round up partial days
    
    # Calculate penalty multiplier (minimum 0, maximum 1)
    penalty_multiplier = max(0.0, 1.0 - (days_late * penalty_per_day))
    
    return True, days_late, penalty_multiplier


def generate_file_path(submission_id: int, filename: str, base_path: str = "uploads/submissions") -> str:
    """
    Generate a secure file path for submission uploads
    
    Args:
        submission_id: The submission ID
        filename: The original filename
        base_path: Base directory for uploads
        
    Returns:
        str: Secure file path
    """
    from werkzeug.utils import secure_filename
    
    secure_name = secure_filename(filename)
    return f"{base_path}/{submission_id}/{secure_name}"


def get_current_utc_time() -> datetime:
    """
    Get current UTC time
    
    Returns:
        datetime: Current UTC datetime
    """
    return datetime.now(timezone.utc)


def safe_float_conversion(value: any, default: float = 0.0) -> float:
    """
    Safely convert a value to float with fallback
    
    Args:
        value: The value to convert
        default: Default value if conversion fails
        
    Returns:
        float: Converted value or default
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def truncate_string(text: str, max_length: int = 255, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length
    
    Args:
        text: The text to truncate
        max_length: Maximum length (including suffix)
        suffix: Suffix to add to truncated text
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
