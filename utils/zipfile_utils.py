from zipfile import ZipFile
from split_file_reader.split_file_writer import SplitFileWriter, counting_file_generator
from utils.env import Env
import os

env = Env()


def zip_files(file_paths: list, zip_file_name: str = "") -> str:
    # writing files to a zipfile
    with ZipFile(zip_file_name + ".zip", "w") as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file, arcname=os.path.basename(file))

    zip_file_path = os.getcwd() + "\\" + zip_file_name + ".zip"
    return zip_file_path


def zip_files_and_remove(file_paths: list, zip_file_name: str = "") -> str:
    with ZipFile(zip_file_name + ".zip", "w") as zip:
        for file in file_paths:
            zip.write(file, arcname=os.path.basename(file))
            os.remove(file)

    zip_file_path = os.getcwd() + "\\" + zip_file_name + ".zip"
    return zip_file_path


def split_file(zip_file_path: str, split_file_name="") -> list[str]:
    with SplitFileWriter(
        # split_file_name + ".zip.",
        counting_file_generator(split_file_name + ".zip.", start_from=1, width=3),
        env.get_value("MAX_CHUNK_SIZE"),
    ) as sfw:
        with ZipFile(file=sfw, mode="w") as zipf:
            zipf.write(zip_file_path, os.path.basename(zip_file_path))

    # get the split file path
    split_files_path = []
    for file in os.listdir(os.getcwd()):
        if file.startswith(split_file_name + ".zip."):
            split_files_path.append(os.getcwd() + "\\" + file)
    return split_files_path


def split_file_and_remove(zip_file_path: str, split_file_name="") -> list[str]:
    with SplitFileWriter(
        # split_file_name + ".zip.",
        counting_file_generator(split_file_name + ".zip.", start_from=1, width=3),
        env.get_value("MAX_CHUNK_SIZE"),
    ) as sfw:
        with ZipFile(file=sfw, mode="w") as zipf:
            zipf.write(zip_file_path, os.path.basename(zip_file_path))
            os.remove(zip_file_path)

    # get the split file path
    split_files_path = []
    for file in os.listdir(os.getcwd()):
        if file.startswith(split_file_name + ".zip."):
            split_files_path.append(os.getcwd() + "\\" + file)
    return split_files_path


if __name__ == "__main__":
    zipFilePath = r"D:\Downloads\Avengers.zip"
    split_file(zipFilePath, "Avengers")
