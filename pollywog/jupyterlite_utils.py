"""
JupyterLite utilities for browser-based file operations.

This module provides helper functions for working with pollywog in JupyterLite,
a browser-based Jupyter environment that runs entirely in the client.
"""

def download_file(content, filename, content_type="application/octet-stream"):
    """
    Trigger a file download in JupyterLite/browser environment.
    
    This function creates a download link in the browser to save generated files
    (like .lfcalc files) directly to the user's computer. In non-browser environments,
    it falls back to saving the file to the current directory.
    
    Args:
        content (str or bytes): File content to download.
        filename (str): Name of the file to download.
        content_type (str): MIME type of the file. 
            Defaults to "application/octet-stream".
    
    Example:
        >>> from pollywog.jupyterlite_utils import download_file
        >>> download_file(b"Hello, world!", "test.txt", "text/plain")
    """
    try:
        from IPython.display import Javascript, display
        import base64
        
        # Convert content to base64 for JavaScript
        if isinstance(content, str):
            content_b64 = base64.b64encode(content.encode('utf-8')).decode('ascii')
        else:
            content_b64 = base64.b64encode(content).decode('ascii')
        
        # JavaScript code to trigger download (handles binary data correctly)
        js_code = f"""
        (function() {{
            const b64 = '{content_b64}';
            const binary = atob(b64);
            const bytes = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) {{
                bytes[i] = binary.charCodeAt(i);
            }}
            const blob = new Blob([bytes], {{type: '{content_type}'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = '{filename}';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }})();
        """
        
        display(Javascript(js_code))
        print(f"Download triggered: {filename}")
        
    except ImportError:
        # Fallback: save to current directory if not in browser
        with open(filename, 'w' if isinstance(content, str) else 'wb') as f:
            f.write(content)
        print(f"File saved: {filename}")

def is_jupyterlite():
    """
    Check if code is running in a JupyterLite environment.
    
    JupyterLite is a browser-based Jupyter distribution that runs entirely
    in the client using Pyodide (Python compiled to WebAssembly). This function
    detects if the current environment is JupyterLite by checking for the
    pyodide module.
    
    Returns:
        bool: True if running in JupyterLite, False otherwise.
    
    Example:
        >>> from pollywog.jupyterlite_utils import is_jupyterlite
        >>> if is_jupyterlite():
        ...     print("Running in browser!")
    """
    try:
        import sys
        return 'pyodide' in sys.modules
    except:
        return False