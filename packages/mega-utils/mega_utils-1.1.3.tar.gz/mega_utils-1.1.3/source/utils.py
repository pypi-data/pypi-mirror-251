"""
This code defines some functions for use with the Mega command line interface.
"""

# Standard imports.
import shutil
import subprocess
from enum import Enum
from getpass import getpass
from pathlib import Path

# Non-standard imports.
from hosker_utils import get_yes_no

#########
# ENUMS #
#########

class GetReturnCode(Enum):
    """ Return codes for any functions which call `mega-get`. """
    FAILURE = 0
    SUCCESS = 1
    PRESENT = 2

#############
# FUNCTIONS #
#############

def run_mega_command(second_half, args=None, quiet=True):
    """ Run a shell command beginning with `mega-`. """
    commands = ["mega-"+second_half]
    local_stdout = subprocess.STDOUT
    if args:
        commands += args
    if quiet:
        local_stdout = subprocess.DEVNULL
    try:
        subprocess.run(commands, check=True, stdout=local_stdout)
    except subprocess.CalledProcessError:
        return False
    return True

def mega_login(username: str, quiet: bool = True) -> bool:
    """ Ronseal. """
    password = getpass(prompt="Enter your Mega password to log in: ")
    return run_mega_command("login", [username, password], quiet=quiet)

def mega_logout(quiet: bool = True) -> bool:
    """ Ronseal. """
    return run_mega_command("logout", quiet=quiet)

def mega_sync(local_path: str, remote_path: str, quiet: bool = True) -> bool:
    """ Sync a given remote folder to its local equivalent. """
    Path(local_path).mkdir(parents=True, exist_ok=True)
    return run_mega_command("sync", [local_path, remote_path], quiet=quiet)

def mega_get_dir(
        url_or_path: str,
        local_path: str,
        auto_delete: bool = False,
        auto_keep: bool = False,
        quiet: bool = True
    ) -> GetReturnCode:
    """ Download a directory at the above URL or remote path to the above local
    path. """
    local_path_obj = Path(local_path)
    if local_path_obj.exists():
        message = (
            "In order to download "+
            url_or_path+
            " to "+
            local_path+
            ", I will need to delete the existing local version. Do you "+
            "wish to proceed?"
        )
        if auto_keep:
            return GetReturnCode.PRESENT
        if auto_delete or get_yes_no(message):
            if not quiet:
                print("Deleting...")
            shutil.rmtree(local_path)
        else:
            if not quiet:
                print(local_path+" already exists.")
            return GetReturnCode.PRESENT
    local_path_obj.mkdir(parents=True)
    success = \
        run_mega_command("get", ["-m", url_or_path, local_path], quiet=quiet)
    if success:
        return GetReturnCode.SUCCESS
    return GetReturnCode.FAILURE

def mega_get(
        url_or_path: str,
        local_path: str,
        quiet: bool = True
    ) -> GetReturnCode:
    """ Download a file at the above URL or remote path to the above local
    path. """
    local_path_obj = Path(local_path)
    if local_path_obj.exists():
        if not quiet:
            print(local_path+" already exists.")
        return GetReturnCode.PRESENT
    success = run_mega_command("get", [url_or_path, local_path], quiet=quiet)
    if success:
        return GetReturnCode.SUCCESS
    return GetReturnCode.FAILURE
