"""This module contains a LoadFlatFile class that contains logic to load flat files in a clean an easy manner."""


import os

import chardet
import clevercsv as csv
import pandas as pd

import logging

logger = logging.getLogger(__name__)


class LoadFlatFile:
    """
    This class contains methods to load and inspect csv files from a directory, and to return them
    as a dictionary of Pandas dataframes.

    Args: 
        file_path (str):                        Path to a file or directory for which we want to 
                                                load the files.
        file_extensions (list, optional):       List of possible file extensions. 
                                                Defaults to csv
        default_encodings (list, optional):     List of possible encodings
                                                Defaults to ascii and utf-8
        possible_delimiters (str, optional):    A string containing the possible delimiters
                                                Defaults to , ; | \t

    """

    def __init__(
        self,
        file_path: str,
        file_extensions: list = ["csv"],
        load_as_varchar = None,
        default_encodings: list = ["ascii", "utf-8"],
        possible_delimiters: str = ",;|\t",
        ):
        assert os.path.exists(file_path), "file_path does not exist."
        
        if os.path.isdir(file_path):
            self.dir_path = os.path.normpath(file_path)
            self.file_path = None
        elif os.path.isfile(file_path):
            extension = os.path.splitext(file_path)[1][1:]
            assert extension in file_extensions, "The extension of the path is not found in the variable file_extensions."
            self.file_path = os.path.normpath(file_path)
            self.dir_path = os.path.dirname(self.file_path)
        self.possible_delimiters = possible_delimiters
        self.file_extensions = file_extensions
        self.load_as_varchar = load_as_varchar
        self.file_paths = []
        self._scan_files(self.dir_path)
        self.file_params = {
            file: {"header": None, "encoding": list(set(default_encodings)), "delimiter": None}
            for file in self.file_paths
        }

        if len(self.file_paths) == 0:
            raise ValueError(
                f"Could not find any .csv files in the directory path {self.dir_path}."
            )

    def load(self, file_paths: list = None) -> dict:
        """
        Calls the functions in this class to read the files and return them in a dict of df's 

        Args:
            file_paths (list, optional): A list of paths to the files. Defaults to None.

        Returns:
            dict_of_dfs: A dictinory of Pandas dataframes
        """
        self.get_encodings(file_paths)
        self.get_delimiter(file_paths)
        self.get_headers(file_paths)
        dict_of_dfs = self.read_files(file_paths)

        return dict_of_dfs

    def _scan_files(self, dir: str) -> None:
        """
        Load all the files with the correct file extension in a directory as a DirEntry into self.file_paths

        Args:
            dir (str): Directory from which to load the files
        """
        if self.file_path:
            for entry in os.scandir(dir):
                if entry.is_file() and entry.path == self.file_path:
                    self.file_paths.append(entry)
                    break
        else:
            for entry in os.scandir(dir):
                if entry.is_file() and entry.name.lower().endswith(tuple(self.file_extensions)):
                    self.file_paths.append(entry)
                elif entry.is_dir():
                    self._scan_files(entry.path)

    def _retrieve_all_encodings(self) -> None:
        """
        Returns a list of lists of the most likely encoding(s) for each file.
        """
        for file in self.file_paths:
            try:
                with open(file, "rb") as rawdata:
                    result = chardet.detect(rawdata.read(10000))
            except Exception as error:  # this exception needs to be more specific
                logger.error(
                    f"Error: chardet encoding of file {file.name} detection failed: {error}"
                )
                try:
                    with open(file) as f:
                        f = str(f)
                except Exception as error:  # this exception needs to be more specific
                    logger.error(
                        f"Error: using the filereader to detect encoding of file {file.name} failed: {error}"
                    )
                else:
                    file_enc = f.split("encoding='")[1].split("'")[0]
            else:
                file_enc = result["encoding"]

            if file_enc not in self.file_params[file]["encoding"]:
                self.file_params[file]["encoding"].insert(0, file_enc)

    def get_encodings(self, file_paths: list = None) -> None:
        """
        Tries to find the encodings for all files in the directory

        Args: 
            file_paths (list, optional): A list of paths to get the encodings from. Defaults to None.

        Returns: 
            None

        """
        files_to_load = self._select_files_to_load(file_paths)
        self._retrieve_all_encodings()
        remove_file = []

        for file_path, params in files_to_load.items():
            for encode in params["encoding"]:
                with open(file_path, "r", encoding=encode) as file:
                    try:
                        file.read(1024)
                        self.file_params[file_path]["encoding"] = encode
                    except UnicodeDecodeError as error:
                        # logger.error(f"Error: the encoding {encode} for file {file.name} does not work, try UTF-8 or ascii: {error}")
                        pass
                    except csv.Error as error:
                        logger.error(
                            f"Error: the file {file.name} contains NULL bytes: {error} \n"
                        )
            if isinstance(params["encoding"], list):
                logger.error(
                    f"Error: the detection of the encoding failed for the file {file_path.name}, this file will not be loaded"
                )
                remove_file.append(file_path)

        for item in remove_file:
            self.file_paths.remove(item)
            del self.file_params[item]

    def get_delimiter(self, file_paths: list = None) -> None:
        """
        Updates the file_params dictionary with the most probable delimiter of the file

        Args: 
            file_paths (list, optional): A list of paths to get the delimiter from. Defaults to None.

        Returns: 
            None

        """
        files_to_load = self._select_files_to_load(file_paths)

        for file_path, params in files_to_load.items():
            with open(file_path, 'r', encoding=params["encoding"]) as file:
                dialect = csv.Sniffer().sniff(file.read(1024), self.possible_delimiters)
                self.file_params[file_path]["delimiter"] = dialect.delimiter

    def get_headers(self, file_paths: list = None) -> None:
        """
        Updates the file_params dictionary with knowledge if file seems to have a header.
        
        Args: 
            file_paths (list, optional): A list of paths to get the headers from. Defaults to None.

        Returns: 
            None

        """
        files_to_load = self._select_files_to_load(file_paths)

        for file_path, params in files_to_load.items():
            with open(file_path, "r", encoding=params["encoding"]) as file:
                if csv.Sniffer().has_header(file.read(1024)):
                    self.file_params[file_path]["header"] = "infer"

    def _select_files_to_load(self, file_paths: list = None) -> dict:
        """
        Check which files we want to load.

        Args:
            file_paths (list, optional): A list of paths to the files. Defaults to None.

        Returns:
            files_to_load (dict): dictionary with the files params to load.
        """
        if file_paths is None:
            files_to_load = self.file_params
        else:
            files_to_load = {
                dir_entry: params 
                for file_path in file_paths 
                for dir_entry, params in self.file_params.items()
                if os.path.normpath(dir_entry.path) == os.path.normpath(file_path)
            }

        return files_to_load

    def read_files(self, file_paths: list = None, load_as_varchar = None) -> dict:
        """
        Reads files and eturns a dictionary of dataframes for each flat file.

        Args:
            file_paths (list, optional): A list of paths to the files. Defaults to None.
            load_as_varchar: the dataframe will be loaded as a string.

        Returns:
            data_dict: A dictinory of dataframes
        """
        files_to_load = self._select_files_to_load(file_paths)

        if load_as_varchar is None:
           load_as_varchar = self.load_as_varchar
            
        assert len(files_to_load) > 0, "There are no files selected to load"

        data_dict = {}

        for file, params in files_to_load.items():
            try:
                                  
                if load_as_varchar:
                    temp_df = pd.read_csv(
                    file,
                    sep=params["delimiter"],
                    encoding=params["encoding"],
                    header=params["header"],
                    dtype=str,
                    na_filter=False    
                    )
                else:
                    temp_df = pd.read_csv(
                    file,
                    sep=params["delimiter"],
                    encoding=params["encoding"],
                    header=params["header"],
                    dtype=None
                    )
            except Exception as error:
                logger.error(f"Error @ file {file.name}: {error}")
            else:
                file_name = os.path.relpath(file.path, self.dir_path)
                data_dict[f"{file_name}"] = temp_df

        return data_dict
