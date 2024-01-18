import os


def path(path: str) -> str:
    return os.path.join(*(path.split("/")))



HOME_DIRECTORY = os.path.expanduser("~")
MODULE_DIR = "kotlyn"
SHELL_SCRIPTS_PATH = path(f"{HOME_DIRECTORY}/{MODULE_DIR}/shell/")
SHELL_FUNCTION_PATH = path(f"{HOME_DIRECTORY}/{MODULE_DIR}/shell/bin")
