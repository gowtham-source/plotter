import logging
import traceback
import re
from typing import Tuple, List, Optional

logger = logging.getLogger(__name__)

# Error types for better categorization
class ErrorType:
    SYNTAX_ERROR = "Syntax Error"
    IMPORT_ERROR = "Import Error"
    NAME_ERROR = "Name Error"
    TYPE_ERROR = "Type Error"
    VALUE_ERROR = "Value Error"
    ATTRIBUTE_ERROR = "Attribute Error"
    RUNTIME_ERROR = "Runtime Error"
    SECURITY_ERROR = "Security Error"
    UNKNOWN_ERROR = "Unknown Error"

# Format error messages for user-friendly display
def format_error_message(error_message: str) -> Tuple[str, str]:
    """Format error messages to be more user-friendly.
    
    Args:
        error_message: The raw error message
        
    Returns:
        Tuple containing (error_type, formatted_message)
    """
    # Extract the error type
    error_type = ErrorType.UNKNOWN_ERROR
    
    if "SyntaxError" in error_message:
        error_type = ErrorType.SYNTAX_ERROR
        # Extract line number and error description
        match = re.search(r"SyntaxError: (.+?)(?:\s+\(line (\d+)\))?$", error_message, re.MULTILINE)
        if match:
            desc = match.group(1)
            line = match.group(2) if match.group(2) else "unknown"
            return error_type, f"Syntax error on line {line}: {desc}"
    
    elif "ImportError" in error_message or "ModuleNotFoundError" in error_message:
        error_type = ErrorType.IMPORT_ERROR
        match = re.search(r"(?:ImportError|ModuleNotFoundError): (.+)$", error_message, re.MULTILINE)
        if match:
            return error_type, f"Import error: {match.group(1)}"
    
    elif "NameError" in error_message:
        error_type = ErrorType.NAME_ERROR
        match = re.search(r"NameError: (.+)$", error_message, re.MULTILINE)
        if match:
            return error_type, f"Name error: {match.group(1)}"
    
    elif "TypeError" in error_message:
        error_type = ErrorType.TYPE_ERROR
        match = re.search(r"TypeError: (.+)$", error_message, re.MULTILINE)
        if match:
            return error_type, f"Type error: {match.group(1)}"
    
    elif "ValueError" in error_message:
        error_type = ErrorType.VALUE_ERROR
        match = re.search(r"ValueError: (.+)$", error_message, re.MULTILINE)
        if match:
            return error_type, f"Value error: {match.group(1)}"
    
    elif "AttributeError" in error_message:
        error_type = ErrorType.ATTRIBUTE_ERROR
        match = re.search(r"AttributeError: (.+)$", error_message, re.MULTILINE)
        if match:
            return error_type, f"Attribute error: {match.group(1)}"
    
    elif "forbidden function" in error_message or "suspicious pattern" in error_message:
        error_type = ErrorType.SECURITY_ERROR
        return error_type, f"Security error: {error_message}"
    
    # Default case for other errors
    return error_type, f"Error: {error_message}"

# Extract Python code from message text
def extract_code(message_text: str) -> Optional[str]:
    """Extract Python code from a message.
    
    Args:
        message_text: The message text that may contain code
        
    Returns:
        The extracted code or None if no code is found
    """
    # Look for code blocks marked with triple backticks
    code_pattern = r'```(?:python)?\s*([\s\S]*?)```'
    match = re.search(code_pattern, message_text)
    
    if match:
        return match.group(1).strip()
    
    # If no code block is found, check if the entire message is code
    if 'import matplotlib' in message_text or 'import plt' in message_text:
        return message_text.strip()
    
    return None

# Format help messages
def get_help_message() -> str:
    """Get the formatted help message for the bot.
    
    Returns:
        Formatted help message string
    """
    return (
        "How to use the Plotting Bot:\n\n"
        "1. Send Python code that creates matplotlib plots\n"
        "2. Make sure your code includes 'plt.show()' to display the plots\n"
        "3. The bot will execute your code and send back the generated images\n\n"
        "All plots will automatically use Times New Roman font.\n\n"
        "Example:\n"
        "```python\n"
        "import matplotlib.pyplot as plt\n"
        "import numpy as np\n\n"
        "x = np.linspace(0, 10, 100)\n"
        "y = np.sin(x)\n\n"
        "plt.plot(x, y)\n"
        "plt.title('Sine Wave')\n"
        "plt.show()\n"
        "```"
    )

def get_welcome_message() -> str:
    """Get the formatted welcome message for the bot.
    
    Returns:
        Formatted welcome message string
    """
    return (
        "Welcome to the Plotting Bot! 📊\n\n"
        "Send me Python code that uses matplotlib to create plots, and I'll execute it and send back the generated images.\n\n"
        "The code should be enclosed in triple backticks like this:\n"
        "```python\n"
        "import matplotlib.pyplot as plt\n"
        "import numpy as np\n\n"
        "x = np.linspace(0, 10, 100)\n"
        "y = np.sin(x)\n\n"
        "plt.plot(x, y)\n"
        "plt.title('Sine Wave')\n"
        "plt.show()\n"
        "```\n\n"
        "All plots will be rendered using Times New Roman font."
    )