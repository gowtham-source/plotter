import os
import sys
import tempfile
import traceback
import contextlib
import io
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import builtins
import importlib
import logging

logger = logging.getLogger(__name__)

# List of allowed modules for the sandbox
ALLOWED_MODULES = {
    'matplotlib', 'matplotlib.pyplot', 'matplotlib.font_manager',
    'numpy', 'pandas', 'scipy', 'seaborn', 'math', 'random',
    'datetime', 'collections', 'itertools', 'functools',
    'os.path', 're', 'json', 'csv'
}

# List of forbidden functions/attributes
FORBIDDEN_ATTRIBUTES = {
    'eval', 'exec', 'compile', 'globals', 'locals', 'open',
    '__import__', 'import_module', 'system', 'popen', 'subprocess',
    'os.system', 'os.popen', 'os.spawn', 'os.exec', 'subprocess.run',
    'subprocess.call', 'subprocess.Popen', 'pty.spawn', 'importlib.import_module'
}

# Restricted import function
def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name not in ALLOWED_MODULES and not any(name.startswith(f"{module}.") for module in ALLOWED_MODULES):
        raise ImportError(f"Import of module '{name}' is not allowed in the sandbox")
    
    # Use the original __import__ function for allowed modules
    return original_import(name, globals, locals, fromlist, level)

# Capture the original __import__ function
original_import = builtins.__import__

# Context manager for the sandbox environment
@contextlib.contextmanager
def sandbox_environment():
    # Create a temporary directory for plots
    temp_dir = tempfile.mkdtemp()
    
    # Save original settings
    original_import_func = builtins.__import__
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    # Create string IO for capturing output
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    try:
        # Replace __import__ with restricted version
        builtins.__import__ = restricted_import
        
        # Redirect stdout and stderr
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        
        # Configure matplotlib for non-interactive backend
        matplotlib.use('Agg')
        
        # Configure font
        font_path = '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'
        if os.path.exists(font_path):
            fm.fontManager.addfont(font_path)
            plt.rcParams['font.family'] = 'Times New Roman'
        
        # Yield the temporary directory and capture objects
        yield temp_dir, stdout_capture, stderr_capture
        
    finally:
        # Restore original settings
        builtins.__import__ = original_import_func
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        
        # Close all matplotlib figures
        plt.close('all')

# Function to execute plotting code safely
def execute_plot_code(code_string):
    plot_files = []
    output = ""
    error = None
    
    with sandbox_environment() as (temp_dir, stdout_capture, stderr_capture):
        try:
            # Prepare the namespace for execution
            namespace = {
                'plt': plt,
                'matplotlib': matplotlib,
                'fm': fm,
                'np': None,  # Will be imported by user code if needed
                'pd': None,  # Will be imported by user code if needed
                '__name__': '__main__',
                '__file__': None,
            }
            
            # Modify the code to save figures instead of showing them
            modified_code = code_string.replace(
                "plt.show()", 
                """\nfor i, fig in enumerate(plt.get_fignums()):\n    fig_obj = plt.figure(i+1)\n    file_path = f'{temp_dir}/plot_{i+1}.png'\n    fig_obj.savefig(file_path, dpi=300, bbox_inches='tight')\n    print(f'Saved plot to {file_path}')\n"""
            )
            
            # Execute the code
            exec(modified_code, namespace)
            
            # Collect output
            output = stdout_capture.getvalue()
            
            # Collect the generated plot files
            for file in os.listdir(temp_dir):
                if file.startswith('plot_') and file.endswith('.png'):
                    plot_files.append(os.path.join(temp_dir, file))
            
        except Exception as e:
            error = f"Error executing plot code: {str(e)}\n{traceback.format_exc()}"
            logger.error(error)
    
    return plot_files, output, error

# Function to check code for potentially harmful operations
def check_code_safety(code_string):
    # Check for forbidden attributes/functions
    for forbidden in FORBIDDEN_ATTRIBUTES:
        if forbidden in code_string:
            return False, f"Code contains forbidden function: {forbidden}"
    
    # Check for suspicious patterns
    suspicious_patterns = [
        "__builtins__", "__dict__", "__class__", "__base__", "__subclasses__",
        "__getattribute__", "__getattr__", "getattr(", "setattr(", "delattr(",
        "read(", "write(", "socket.", "connect(", "bind(", "listen(",
        "requests.", "urllib", "http", "ftp", "smtp", "telnet"
    ]
    
    for pattern in suspicious_patterns:
        if pattern in code_string:
            return False, f"Code contains suspicious pattern: {pattern}"
    
    return True, None