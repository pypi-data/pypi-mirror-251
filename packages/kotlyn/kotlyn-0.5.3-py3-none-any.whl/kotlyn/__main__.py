import zenyx
from zenyx import printf

import os
import sys
import random
import time


from kotlyn.Paths import *
import kotlyn.Files as Files
import kotlyn.Environ as Environ
import kotlyn.Download as Download


def main() -> None:
    ARGS = zenyx.Arguments(sys.argv)
    original_path = os.path.realpath("./")
    kotlyn_cmd_filename = "kotlyn.ps1"

    if len(ARGS.normals) < 1:
        return

    if ARGS.tagged("--verbose"):
        printf(f"ARGS: {ARGS.args}")

    if not ARGS.normals[0].startswith("!") and len(ARGS.tags) == 0:
        ARGS.tags.append("run")

    if ARGS.normals[0] == "!setup":
        printf("@!Kotlyn - Kotlin | Setup$&")
        printf(
            "@~Installing kotlin (.kt) language, creating Environment variables...$&"
        )

        # Creating folders
        Files.directory.create(f"{MODULE_DIR}")
        Files.directory.create(f"{MODULE_DIR}/shell")
        Files.directory.create(f"{MODULE_DIR}/shell/bin")
        Files.directory.create(f"{MODULE_DIR}/temp/install")

        # Creating files
        Files.file.create(path(f"{HOME_DIRECTORY}/{MODULE_DIR}/{MODULE_DIR}.toml"))
        Files.file.create(path(f"{HOME_DIRECTORY}/{MODULE_DIR}/.builder_install"))

        # Safety check for a complete install
        builder_install_info = Files.file.read(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/.builder_install")
        )
        if builder_install_info == "COMPLETE":
            printf("@!Setup has been completed before!$&")
            return

        # Downloading latest release
        printf("  @?Downloading Kotlin...$&", end="\r")

        Download.get_github_release(
            "JetBrains", "kotlin", path(f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/install")
        )
        zip_name: str = Files.directory.find_kotlin_compiler_zip(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/install")
        )
        compiler_zip_path = path(
            f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/install/{zip_name}"
        )

        printf("  Kotlin Downloaded", end="\r")

        # Unspacking zip
        printf("  @?Unpacking ZIP Archive...$&", end="\r")

        Files.unpack_zip(compiler_zip_path, path(f"{HOME_DIRECTORY}/{MODULE_DIR}/"))
        Files.directory.delete_all_files(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/install")
        )

        printf("  Unpacked ZIP Archive", end="\r")

        kb_kotlin_home_path = path(f"{HOME_DIRECTORY}/{MODULE_DIR}/kotlinc")
        if not os.path.exists(kb_kotlin_home_path):
            raise Exception(
                "The path which the builder would use for Environment variables is not available"
            )

        # Set up cmd tool
        Files.file.write(
            path(f"{SHELL_FUNCTION_PATH}/{kotlyn_cmd_filename}"),
            "\n".join(
                [
                    # Combine all arguments into a single string
                    '$argsString = ""',
                    "while ($args) {",
                    '    $argsString += " " + $args[0]',
                    "    $args = $args[1..$args.length]",
                    "}",
                    # Call the Python module with the combined arguments and capture the output
                    'Invoke-Expression -Command "python -m kotlyn $argsString"',
                ]
            ),
        )

        # Environment Handling
        env_handler = Environ.get_OSEnvironment(
            path(f"{SHELL_SCRIPTS_PATH}/kotlyn_setup.[ext]")
        )
        env_handler.set_environment_variable(
            "KOTLIN_HOME", path(f"{HOME_DIRECTORY}/{MODULE_DIR}/kotlinc")
        )
        env_handler.update_path(path("%KOTLIN_HOME%/bin"))
        env_handler.update_path(f"{SHELL_FUNCTION_PATH}")
        env_handler.push()

        # Confirm Install Success
        Files.file.write(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/.builder_install"), "COMPLETE"
        )
        printf.clear_screen()
        printf("@!Kotlyn - Kotlin | Installed$&")
        return

    builder_install_info = Files.file.read(
        path(f"{HOME_DIRECTORY}/{MODULE_DIR}/.builder_install")
    )
    if builder_install_info != "COMPLETE":
        printf("@!Setup has not been completed!$&\nRun setup: python -m kotlyn !setup")
        return

    if ARGS.normals[0] == "!version":
        print("[Builder/CLI] \nKotlyn version 0.0.7")
        os.system("echo [JetBrains/Kotlin] && kotlin -version")

    if ARGS.normals[0] == "!update":
        os.system("python -m pip install --upgrade kotlyn")

    if ARGS.tagged("build"):
        if len(ARGS.normals) < 1 or ARGS.normals[0].startswith("!"):
            printf("@!Missing param(s): <filename>$&")
            return

        os.system(
            f"cd {os.path.dirname(ARGS.normals[0])} && kotlinc {os.path.realpath(ARGS.normals[0])} -include-runtime -d Main.jar {Files.directory.list_not_entry_kt(os.path.dirname(ARGS.normals[0]), ARGS.normals[0])}"
        )

    if ARGS.tagged("run"):
        if len(ARGS.normals) < 1 or ARGS.normals[0].startswith("!"):
            printf("@!Missing param(s): <filename>$&")
            return

        jar_path = path(
            f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/kotlyn-{time.time()}-{random.randint(100000, 999999)}-{random.randint(100000, 999999)}"
        )

        os.system(
            f"cd {os.path.dirname(ARGS.normals[0])} && kotlinc {os.path.realpath(ARGS.normals[0])} -include-runtime -d {jar_path}.jar {Files.directory.list_not_entry_kt(os.path.dirname(ARGS.normals[0]), ARGS.normals[0])} && java -jar {jar_path}.jar"
        )
        os.remove(f"{jar_path}.jar")


if __name__ == "__main__":
    main()
