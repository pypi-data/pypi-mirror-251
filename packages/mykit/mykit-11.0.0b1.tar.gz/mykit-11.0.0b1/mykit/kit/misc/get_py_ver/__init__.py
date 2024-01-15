import sys as _sys
def get_py_ver() -> str:
    """Get the current Python version in the expected 'Major.minor.patch' format"""
    info = _sys.version_info
    M = info.major  
    m = info.minor  
    p = info.micro  
    return f'{M}.{m}.{p}'