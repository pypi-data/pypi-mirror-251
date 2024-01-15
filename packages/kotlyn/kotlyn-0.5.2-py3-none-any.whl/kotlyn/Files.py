import os
import zipfile
from kotlyn.Paths import *
from zenyx import printf


class file:
    @classmethod
    def create(this, filepath: str) -> None:
        if os.path.exists(filepath):
            return
        with open(filepath, "w") as wf:
            wf.write("")

    @classmethod
    def write(this, filepath: str, content: str) -> None:
        with open(filepath, "w") as wf:
            wf.write(content)

    @classmethod
    def read(this, filepath: str) -> str:
        res = ""
        with open(filepath, "r") as rf:
            res = rf.read()
        return res


class directory:
    @classmethod
    def create(this, directory_name: str) -> None:
        """THIS WILL CREATE A DIRECTORY IN THE USER'S HOME (~) DIRECTORY

        Args:
            directory_name (str): name of the dir
        """

        folder_path = os.path.join(HOME_DIRECTORY, directory_name)

        try:
            os.makedirs(folder_path)
            printf(
                f"  @!Kotlyn.files$&/directory.create\n   @~Directory '{directory_name}' created successfully$&"
            )
        except FileExistsError:
            printf(
                f"  @!Kotlyn.files$&/directory.create\n   @~Directory {directory_name}' already exists$&"
            )
        except Exception as e:
            printf(f"An error occurred: {e}")

    @classmethod
    def delete_all_files(this, directory_path: str) -> None:
        try:
            # Get the list of files in the folder
            files = os.listdir(directory_path)

            # Iterate through the files and delete each one
            for file_name in files:
                file_path = os.path.join(directory_path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            printf(
                f"  @!Kotlyn.files$&/directory.delete_all_files\n   @~All files in {directory_path} have been deleted.$&"
            )
        except Exception as e:
            printf(f"An error occurred: {e}")

    @classmethod
    def find_kotlin_compiler_zip(this, directory_path):
        try:
            files = os.listdir(directory_path)
            matching_files = [
                file
                for file in files
                if file.startswith("kotlin-compiler-") and file.endswith(".zip")
            ]

            if matching_files:
                return matching_files[0]
            else:
                printf(
                    "  @!Kotlyn$&/find_kotlin_compiler_zip\n   @~No matching file found.$&"
                )
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @classmethod
    def list_not_entry_kt(this, filepath: str, entry: str):
        files = os.listdir(os.path.realpath(filepath))
        return " ".join([file for file in files if file != entry and file.endswith(".kt")])

def unpack_zip(zip_path, output_directory):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_directory)
        printf(f"  @!Kotlyn$&/unpack_zip\n   @~Zip file unpacked successfully$&")
    except zipfile.BadZipFile:
        printf(
            f"  @!Kotlyn$&/unpack_zip\n   @~The file '{zip_path}' is not a valid zip archive.$&"
        )
    except Exception as e:
        printf(f"An error occurred: {e}")
