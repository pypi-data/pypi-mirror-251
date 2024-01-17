"""
This code defines some functions for use with the Mega command line interface.
"""

# Standard imports.
import subprocess
from getpass import getpass
from pathlib import Path

#############
# FUNCTIONS #
#############

def run_mega_command(second_half, args=None):
    """ Run a shell command beginning with `mega-`. """
    commands = ["mega-"+second_half]
    if args:
        commands += args
    try:
        subprocess.run(commands, check=True)
    except subprocess.CalledProcessError:
        return False
    return True

def run_mega_command_and_return_output(second_half, args=None):
    """ Run a shell command beginning with `mega-`, and capture the output. """
    commands = ["mega-"+second_half]
    success = True
    output = None
    if args:
        commands += args
    try:
        process = subprocess.run(commands, check=True, capture_output=True)
        output = process.stdout
    except subprocess.CalledProcessError:
        success = False
    return success, output

def report(success):
    """ Report on whether a given Mega command succeeded or not. """
    if success:
        print("Done.")
    else:
        print("Failed.")

def mega_login(username: str) -> bool:
    """ Ronseal. """
    password = getpass(prompt="Enter your Mega password to log in: ")
    print("Logging in...")
    success = run_mega_command("login", [username, password])
    report(success)
    return success

def mega_logout() -> bool:
    """ Ronseal. """
    success = run_mega_command("logout")
    report(success)
    return success

def mega_sync(local_path: str, remote_path: str) -> bool:
    """ Sync a given remote folder to its local equivalent. """
    Path(local_path).mkdir(parents=True, exist_ok=True)
    print(
        "Syncing remote folder "+
        remote_path+
        " to local folder "+
        local_path+
        "..."
    )
    success = run_mega_command("sync", [local_path, remote_path])
    report(success)
    return success

def mega_get(url: str, local_path: str) -> bool:
    """ Download a file at the above URL to the above local path. """
    if Path(local_path).exists():
        print(local_path+" already exists.")
        return True
    print("Dowloading to "+local_path+"...")
    success = run_mega_command("get", [url, local_path])
    report(success)
    return success
