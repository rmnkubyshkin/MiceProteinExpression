import csv
from os import makedirs, listdir
from os.path import isdir, join
from datetime import datetime
from re import split, match
import json
from shutil import rmtree, move, copy
import pandas as pd
import inspect

from package.logging.LoggingClass import Logging
from package.utils.FolderConstantsClass import training_converted_raw_data_folder


class Validation:

    def __init__(self,
                 logger,
                 schema_path,
                 raw_data_folder,
                 converted_folder,
                 bad_raw_folder,
                 good_raw_folder
                 ):

        self.logger = logger
        self.schema_path = schema_path
        self.bad_raw_folder = bad_raw_folder
        self.good_raw_folder = good_raw_folder
        self.batch_folder = raw_data_folder
        self.converted_folder = converted_folder

    def delete_existing_good_raw_data_folder(self, good_raw_folder):
        try:
            self.logger.enter_into_method(inspect.stack()[0][3])

            self.delete_directory_if_exist(good_raw_folder)

            self.logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error while creating directory {e}'
            self.logger.exception(log_message, e)
            raise e

    def delete_existing_bad_raw_data_folder(self, bad_raw_folder):
        try:
            self.logger.enter_into_method(inspect.stack()[0][3])

            self.delete_directory_if_exist(bad_raw_folder)

            self.logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error while deleting directory {e}'
            self.logger.exception(log_message, e)
            raise e

    def delete_existing_converted_raw_data_folder(self, converted_raw_folder):
        try:
            self.logger.enter_into_method(inspect.stack()[0][3])

            self.delete_directory_if_exist(converted_raw_folder)

            self.logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error while deleting directory {e}'
            self.logger.exception(log_message, e)
            raise e

    def create_bad_raw_data_folder(self, bad_raw_folder):
        try:
            self.logger.enter_into_method(inspect.stack()[0][3])

            self.create_directory_if_not_exist(bad_raw_folder)

            self.logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error while creating directory {e}'
            self.logger.exception(log_message, e)
            raise e

    def create_good_raw_data_folder(self, good_raw_folder):
        try:
            self.logger.enter_into_method(inspect.stack()[0][3])

            self.create_directory_if_not_exist(good_raw_folder)

            self.logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error while creating directory {e}'
            self.logger.exception(log_message, e)
            raise e

    def create_converted_raw_data_folder(self, converted_raw_folder):
        try:
            self.logger.enter_into_method(inspect.stack()[0][3])

            self.create_directory_if_not_exist(converted_raw_folder)

            self.logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error while creating directory {e}'
            self.logger.exception(log_message, e)
            raise e

    def create_directory_if_not_exist(self, data_folder):
        self.logger.enter_into_method(inspect.stack()[0][3])

        if not isdir(data_folder):
            makedirs(data_folder)
            self.logger.write_message_from_method(f'Folder: {data_folder} create successful!')

        self.logger.exited_from_method(inspect.stack()[0][3])

    def delete_directory_if_exist(self, data_folder):
        self.logger.enter_into_method(inspect.stack()[0][3])

        if isdir(data_folder):
            rmtree(data_folder)
            self.logger.write_message_from_method(f'Folder: {data_folder} delete successful!')

        self.logger.exited_from_method(inspect.stack()[0][3])

    def manual_regex_creation(self):
        return "['Data']+['\_'']+['Cortex']+['\_'']+['Nuclear']+['\_'']+[\#]+[\d]+\.csv"

    def get_values_from_schema(self, log_file_path):
        self.logger.enter_into_method(inspect.stack()[0][3])
        try:
            with open(self.schema_path, 'r') as f:
                dictionary = json.load(f)
                f.close()
            file_name = dictionary['file_name']
            file_number = dictionary['file_number']
            column_names = dictionary['column_names']
            num_of_columns = dictionary['num_of_columns']

            log_message = (f'file_name:: {file_name},'
                           f'file_number:: {file_number},'
                           f'column_names:: {column_names},'
                           f'num_of_columns:: {num_of_columns}'
                           )
            self.logger.write_message_from_method(log_message)
            self.logger.exited_from_method(inspect.stack()[0][3])
        except ValueError as e:
            log_message = "ValueError: Value not found inside schema_training.json"
            self.logger.exception(log_message, e)
            raise e
        except KeyError as e:
            log_message = "KeyError: Key not found inside schema_training.json"
            self.logger.exception(log_message, e)
            raise e
        except Exception as e:
            self.logger.exception("Exception", e)
            raise e

        return file_name, file_number, column_names, num_of_columns

    def convert_xls_to_csv(self):
        self.logger.enter_into_method(inspect.stack()[0][3])
        self.delete_existing_converted_raw_data_folder(self.converted_folder)
        self.create_converted_raw_data_folder(self.converted_folder)
        files_to_validate = [f for f in listdir(self.batch_folder)]
        try:
            for filename in files_to_validate:
                read_file = pd.read_excel(self.batch_folder + filename)
                split_filename_at_dot = split('.xls', filename)
                path_to_save = self.converted_folder + split_filename_at_dot[0] + '.csv'
                read_file.to_csv(path_to_save, index=None, header=True)
            self.logger.exited_from_method(inspect.stack()[0][3])
            return
        except OSError as e:
            log_message = f'Error occurred {e}'
            self.logger.exception(log_message, e)
            raise e

    def validate_num_of_columns(self, num_of_columns):
        self.logger.enter_into_method(inspect.stack()[0][3])

        try:
            self.check_list_of_files_for_wrong_num_of_columns(num_of_columns)

            self.logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error occurred while moving the file: {e}'
            self.logger.exception(log_message, e)
        except Exception as e:
            log_message = f'Error occurred {e}'
            self.logger.exception(log_message, e)
            raise e

    def check_list_of_files_for_wrong_num_of_columns(self, num_of_columns):
        self.logger.enter_into_method(inspect.stack()[0][3])

        for file_name in listdir(self.converted_folder):
            self.check_file_for_wrong_num_of_columns(file_name, num_of_columns)

        self.logger.exited_from_method(inspect.stack()[0][3])

    def check_file_for_wrong_num_of_columns(self, file_name, num_of_columns):
        self.logger.enter_into_method(inspect.stack()[0][3])

        csv = pd.read_csv(self.converted_folder + file_name)
        if csv.shape[1] != num_of_columns:
            move(self.converted_folder + file_name, self.bad_raw_folder)
            log_message = f'Invalid num of columns for the file, moved to {self.bad_raw_folder}'
            self.logger.write_message_from_method(log_message)
        else:
            log_message = "Num of column validation completed!"
            self.logger.write_message_from_method(log_message)
            self.logger.exited_from_method(inspect.stack()[0][3])

