"""
JupyterLite utilities for browser-based file operations.

This module provides helper functions for working with pollywog in JupyterLite,
a browser-based Jupyter environment that runs entirely in the client.
"""
from IPython.display import Javascript, display

def ensure_comm_target():
    """
    Ensure the JavaScript comm target for pollywog downloads is registered in the notebook frontend.

    This function injects JavaScript that registers a comm target named 'pollywog_download'.
    When a comm message is sent from Python, the frontend receives the file data and triggers a browser download.
    The registration is only performed once per session, using a window-level flag to avoid duplicates.

    Should be called before sending download comm messages from Python.
    """
    js_code = """
    if (!window.pollywog_comm_registered) {
        window.pollywog_comm_registered = true;
        if (typeof Jupyter !== 'undefined' && Jupyter.notebook && Jupyter.notebook.kernel) {
            Jupyter.notebook.kernel.comm_manager.register_target('pollywog_download', function(comm) {
                comm.on_msg(function(msg) {
                    var data = msg.content.data;
                    var b64 = data.content_b64;
                    var filename = data.filename;
                    var content_type = data.content_type;
                    var binary = atob(b64);
                    var bytes = new Uint8Array(binary.length);
                    for (var i = 0; i < binary.length; i++) {
                        bytes[i] = binary.charCodeAt(i);
                    }
                    var blob = new Blob([bytes], {type: content_type});
                    var url = URL.createObjectURL(blob);
                    var a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                });
            });
        }
    }
    """
    display(Javascript(js_code))

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
    ensure_comm_target()
    import base64
    from IPython import get_ipython

    # Convert content to base64
    if isinstance(content, str):
        content_b64 = base64.b64encode(content.encode('utf-8')).decode('ascii')
    else:
        content_b64 = base64.b64encode(content).decode('ascii')

    ip = get_ipython()
    if ip is not None and hasattr(ip, 'kernel'):
        comm = ip.kernel.comm_manager.new_comm('pollywog_download')
        comm.send({
            'content_b64': content_b64,
            'filename': filename,
            'content_type': content_type
        })
        print(f"Download triggered: {filename}")
    else:
        # Fallback for non-JupyterLite environments
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