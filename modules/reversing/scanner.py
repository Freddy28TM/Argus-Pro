import os

def check_file_type(filepath):
    """Detects if a file is an ELF (Linux), PE (Windows), or Script."""
    try:
        with open(filepath, 'rb') as f:
            header = f.read(4)
            if header == b'\x7fELF':
                return "Linux Executable (ELF)"
            elif header == b'MZ':
                return "Windows Executable (PE)"
            elif header.startswith(b'\xff\xd8'):
                return "JPEG Image"
            else:
                return "Unknown/Data Binary"
    except Exception as e:
        return f"Error reading file: {e}"
