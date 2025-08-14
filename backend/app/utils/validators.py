"""
Validation utility functions for the CSRS Automated Assessment System
"""

from enum import Enum
from typing import List, Any


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Validate that a filename has an allowed extension
    
    Args:
        filename: The filename to validate
        allowed_extensions: List of allowed extensions (with or without dots)
        
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    # Normalize extensions (remove dots if present)
    normalized_allowed = [ext.lstrip('.').lower() for ext in allowed_extensions]
    
    return extension in normalized_allowed


def validate_enum_value(value: Any, enum_class: Enum) -> bool:
    """
    Validate that a value is a valid enum member
    
    Args:
        value: The value to validate
        enum_class: The enum class to validate against
        
    Returns:
        bool: True if value is valid enum member, False otherwise
    """
    try:
        if isinstance(value, str):
            # Try to find enum by value
            return value in [e.value for e in enum_class]
        else:
            # Try direct enum validation
            return value in enum_class
    except (ValueError, TypeError):
        return False


def validate_required_fields(data: dict, required_fields: List[str]) -> List[str]:
    """
    Check for missing required fields in request data
    
    Args:
        data: Dictionary of request data
        required_fields: List of required field names
        
    Returns:
        List[str]: List of missing field names
    """
    return [field for field in required_fields 
            if field not in data or data[field] is None or data[field] == ""]


def validate_positive_integer(value: Any, field_name: str = "value") -> tuple[bool, str]:
    """
    Validate that a value is a positive integer
    
    Args:
        value: The value to validate
        field_name: Name of the field for error messages
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        int_value = int(value)
        if int_value <= 0:
            return False, f"{field_name} must be a positive integer"
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} must be a valid integer"
