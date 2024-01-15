from zenyx import printf
from kotlyn.Paths import *
import kotlyn.Files as Files
import platform
import os


class OSEnvironment:
    def __init__(this, res_file_path: str) -> None:
        this.setup_file = ""
        this.res_file_path = res_file_path
        pass

    def __raise_not_implemented_error(this):
        raise NotImplementedError("Fallback, your choice of os is not implemented yet!")

    def set_environment_variable(this, name: str, value: str) -> None:
        this.__raise_not_implemented_error()

    def update_path(this, file_path: str) -> None:
        this.__raise_not_implemented_error()

    def push(this) -> None:
        this.__raise_not_implemented_error()


class Windows(OSEnvironment):
    def __init__(this, res_file_path) -> None:
        super().__init__(res_file_path)

    def set_environment_variable(this, name: str, value: str) -> None:
        this.setup_file += "\n".join(
            [
                f"# ------------------------------------------------------ [Environment Operation Begins] -----------------------------------------------------",
                f'[Environment]::SetEnvironmentVariable("{name}", "{value}", [EnvironmentVariableTarget]::User)',
                f"# ------------------------------------------------------- [Environment Operation Ends] ------------------------------------------------------\n\n",
            ]
        )

    def update_path(this, file_path: str) -> None:
        this.setup_file += "\n".join(
            [
                f"# ---------------------------------------------------------- [PATH Operation Begins] --------------------------------------------------------",
                f'$InstallLocation = "{file_path}"',
                # To add folder to PATH
                "$persistedPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::User) -split ';'",
                "if ($persistedPath -notcontains $InstallLocation) {",
                "   $persistedPath = $persistedPath + $InstallLocation | where { $_ }",
                "   [Environment]::SetEnvironmentVariable('Path', $persistedPath -join ';', [EnvironmentVariableTarget]::User)",
                "}",
                # To verify if PATH isn't already added
                "$envPaths = $env:Path -split ';'",
                "if ($envPaths -notcontains $InstallLocation) {",
                "   $envPaths = $envPaths + $InstallLocation | where { $_ }",
                "   $env:Path = $envPaths -join ';'",
                "}",
                f"# ----------------------------------------------------------- [PATH Operation Ends] ---------------------------------------------------------\n\n",
            ]
        )

    def push(this) -> None:

        if not this.res_file_path.endswith(".ps1"):
            raise ValueError("On a windows system the res file must be a .ps1 file")

        Files.file.create(this.res_file_path)
        Files.file.write(this.res_file_path, this.setup_file)
        os.system("powershell " + this.res_file_path)


class Linux(OSEnvironment):
    def __init__(this, res_file_path) -> None:
        super().__init__(res_file_path)


class MacOS(OSEnvironment):
    def __init__(this, res_file_path) -> None:
        super().__init__(res_file_path)


def get_OSEnvironment(res_path: str) -> OSEnvironment:
    """Returns an OS specific handler for your environment variable setup

    Args:
        res_path (str): SHOULD NOT HAVE FILE EXTENSION, just use `.[ext]`

    Returns:
        OSEnvironment: the environment handler
    """

    def swap_ext(original: str, to: str):
        return original.replace("[ext]", to)

    print(str(platform.system()).lower())

    match str(platform.system()).lower():
        case "windows":
            return Windows(swap_ext(res_path, "ps1"))
        case "linux":
            return Linux(res_path)
        case "macos":
            return MacOS(res_path)
