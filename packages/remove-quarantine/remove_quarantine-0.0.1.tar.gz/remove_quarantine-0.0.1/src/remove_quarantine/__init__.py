# homekitlink_ffmpeg/__init__.py
# version 0.0.25
#
#
import os



def show_logging():
    """Get the path to the appropriate FFmpeg binary."""
    # __file__ is the path to the current file (__init__.py)
    # We loop back to the directory of __init__.py and build the path from there
    package_dir = os.path.abspath(os.path.dirname(__file__))
    log_file_path = os.path.join(package_dir, 'post_install.log')
    try:
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            return(log_file.read())
    except FileNotFoundError:
        print(f"Log file not found at {log_file_path}")