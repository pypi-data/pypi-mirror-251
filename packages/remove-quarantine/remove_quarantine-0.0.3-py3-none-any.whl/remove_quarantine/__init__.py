# homekitlink_ffmpeg/__init__.py
# version 0.0.25
#
#
import os
import subprocess
import traceback
from glob import glob
from threading import Thread


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
        return (f"Log file not found at {log_file_path}")

def _remove_quarantine_thread(plugin_paths, log_file_path):
    base_command = '/usr/bin/xattr -rd com.apple.quarantine'
    #delay_between_commands = 0.1  # Delay in seconds (adjust as needed)
    with open(log_file_path, 'a') as log_file:
        for plugin_path in plugin_paths:
            command = f"{base_command} '{plugin_path}'"
            log_file.write(f"Trying the following: {command}\n")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                log_file.write(f"Successfully removed quarantine attribute from {plugin_path}\n")
                log_file.write(result.stdout)
            else:
                log_file.write(f"Failed to remove quarantine attribute from {plugin_path}:\n")
                log_file.write(result.stderr)
                log_file.write(result.stdout)
            if result.stdout or result.stderr:
                log_file.write(result.stdout)
                log_file.write(result.stderr)

def remove_quarantine():
    try:
    # Run the standard install process
        package_dir = os.path.abspath(os.path.dirname(__file__))
        indigo_plugins_path = '/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins'
        indigo_disabled_plugins_path = '/Library/Application Support/Perceptive Automation/Indigo 2023.2/Plugins (Disabled)'
        log_file_path = os.path.join(package_dir, 'remove_quarantine', 'post_install.log')
        plugin_paths = glob(os.path.join(indigo_plugins_path, '*.indigoPlugin'))
        plugin_paths += glob(os.path.join(indigo_disabled_plugins_path, '*.indigoPlugin'))
        # Construct the base xattr command to remove the quarantine attribute
        base_command = '/usr/bin/xattr -rd com.apple.quarantine'
        quarantine_thread = Thread(target=_remove_quarantine_thread, args=(plugin_paths, log_file_path))
        quarantine_thread.start()
        quarantine_thread.join()  # Optionally wait for the thread to finish

        return show_logging()

    except Exception as e:
        print("An unexpected error occurred: ", e)
        print(traceback.format_exc())
        raise  # Re-raise the exception to ensure it's not silently ignored