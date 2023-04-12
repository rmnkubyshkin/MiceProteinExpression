from os import makedirs, listdir
from os.path import isdir
from re import split, match
import json
from shutil import rmtree, move
import pandas as pd
import inspect

from package.utils.FileOperationClass import FileOperation
from package.schemas.ValidationSchemaOperationsClass import TrainingSchemaOperations


class Validation:

    def __init__(self,
                 logger,
                 raw_data_folder,
                 converted_folder,
                 bad_raw_folder,
                 good_raw_folder,
                 ):

        self.validation_logger = logger
        self.bad_raw_folder = bad_raw_folder
        self.good_raw_folder = good_raw_folder
        self.batch_folder = raw_data_folder
        self.converted_folder = converted_folder
        self.schema = TrainingSchemaOperations()
        self.file_operation = FileOperation()

    def manual_regex_creation(self):
        return "['Data']+['\_'']+['Cortex']+['\_'']+['Nuclear']+['\_'']+[\#]+([0-9]|[1-9][0-9]|[1-9][0-9][0-9])+\.csv"

    def convert_xls_to_csv(self):
        self.validation_logger.enter_into_method(inspect.stack()[0][3])
        self.file_operation.delete_existing_data_folder(self.converted_folder)
        self.file_operation.create_data_folder(self.converted_folder)

        try:
            files_to_validate = [f for f in listdir(self.batch_folder)]

            for filename in files_to_validate:
                read_file = pd.read_excel(self.batch_folder + filename)
                split_filename_at_dot = split('.xls', filename)
                path_to_save = self.converted_folder + split_filename_at_dot[0] + '.csv'
                read_file.to_csv(path_to_save, index=None, header=True)
            self.validation_logger.exited_from_method(inspect.stack()[0][3])
            return
        except OSError as e:
            log_message = f'Error occurred {e}'
            self.validation_logger.exception(log_message, e)
            raise e

    def validate_num_of_columns(self):
        self.validation_logger.enter_into_method(inspect.stack()[0][3])

        try:
            self.file_operation.delete_existing_data_folder(self.bad_raw_folder)
            self.file_operation.delete_existing_data_folder(self.good_raw_folder)
            self.file_operation.create_data_folder(self.good_raw_folder)
            self.file_operation.create_data_folder(self.bad_raw_folder)
            self.__check_list_of_files_for_wrong_num_of_columns()

            self.validation_logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error occurred while moving the file: {e}'
            self.validation_logger.exception(log_message, e)
        except Exception as e:
            log_message = f'Error occurred {e}'
            self.validation_logger.exception(log_message, e)
            raise e

    def validate_missing_all_column_values_in_folder(self):
        try:
            self.validation_logger.enter_into_method(inspect.stack()[0][3])

            for file in listdir(self.good_raw_folder):
                self.__validate_missing_all_column_values_in_file(file)
        except OSError as e:
            log_message = f'Error occurred while moving the file: {e}'
            self.validation_logger.exception(log_message, e)
        except Exception as e:
            log_message = f'Error occurred {e}'
            self.validation_logger.exception(log_message, e)
            raise e

    def validate_name_of_columns(self):
        try:
            self.validation_logger.enter_into_method(inspect.stack()[0][3])

            self.__check_list_of_files_for_wrong_name_of_columns()

            self.validation_logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error occurred while moving the file: {e}'
            self.validation_logger.exception(log_message, e)
        except Exception as e:
            log_message = f'Error occurred {e}'
            self.validation_logger.exception(log_message, e)
            raise e

    def validate_file_name(self):
        self.validation_logger.enter_into_method(inspect.stack()[0][3])

        files_to_validate = [f for f in listdir(self.good_raw_folder)]
        self.__check_list_of_files_for_wrong_file_name(files_to_validate)

        self.validation_logger.exited_from_method(inspect.stack()[0][3])

    def __check_list_of_files_for_wrong_num_of_columns(self):
        self.validation_logger.enter_into_method(inspect.stack()[0][3])

        for file_name in listdir(self.converted_folder):
            self.__check_file_for_wrong_num_of_columns(file_name)

        self.validation_logger.exited_from_method(inspect.stack()[0][3])

    def __check_list_of_files_for_wrong_file_name(self, files_to_validate):
        self.validation_logger.enter_into_method(inspect.stack()[0][3])

        try:
            for file_name in files_to_validate:
                self.__check_file_for_equal_of_regex(file_name)

            self.validation_logger.exited_from_method(inspect.stack()[0][3])
        except Exception as e:
            log_message = f'Error occurred while validating file: {e}'
            self.validation_logger.write_message_from_method(log_message)
            raise e

    def __validate_missing_all_column_values_in_file(self, file):
        file_from_good_folder = pd.read_csv(self.good_raw_folder + file)
        count = 0
        for columns in file_from_good_folder:
            count_of_whole_values = len(file_from_good_folder[columns])
            count_of_null_values = file_from_good_folder[columns].count()
            if count_of_whole_values - count_of_null_values == count_of_whole_values:
                count += 1
                move(self.good_raw_folder + file, self.bad_raw_folder)
                log_message = f'Invalid count of values in column in file: {file} ' \
                              f'File moved to Bad Raw Folder'
                self.validation_logger.write_message_from_method(log_message)
                break
        if count == 0:
            file_from_good_folder.to_csv(self.good_raw_folder + file, index=None, header=True)

    def __check_list_of_files_for_wrong_name_of_columns(self):
        self.validation_logger.enter_into_method(inspect.stack()[0][3])

        for file_name in listdir(self.good_raw_folder):
            self.__check_file_for_wrong_name_of_columns(file_name)

        self.validation_logger.exited_from_method(inspect.stack()[0][3])

    def __check_file_for_wrong_num_of_columns(self, file_name):
        self.validation_logger.enter_into_method(inspect.stack()[0][3])
        values_from_schema = self.schema.get_values_from_schema()
        _csv = pd.read_csv(self.converted_folder + file_name)
        if _csv.shape[1] != values_from_schema[3]:
            move(self.converted_folder + file_name, self.bad_raw_folder)
            log_message = f'Invalid num of columns for the file, moved to {self.bad_raw_folder}'
            self.validation_logger.write_message_from_method(log_message)
        else:
            move(self.converted_folder + file_name, self.good_raw_folder)
            log_message = "Num of column validate completed!"
            self.validation_logger.write_message_from_method(log_message)

        self.validation_logger.exited_from_method(inspect.stack()[0][3])

    def __check_file_for_equal_of_regex(self, file_name):
        self.validation_logger.enter_into_method(inspect.stack()[0][3])

        regex = self.manual_regex_creation()
        if match(regex, file_name):
            log_message = f'File name: {file_name} is valid, file moved to good_raw folder'
            self.validation_logger.write_message_from_method(log_message)
        else:
            move(self.good_raw_folder + file_name, self.bad_raw_folder)
            log_message = f'File name:{file_name} is invalid, file moved to bad_raw folder'
            self.validation_logger.write_message_from_method(log_message)

        self.validation_logger.exited_from_method(inspect.stack()[0][3])

    def __check_file_for_wrong_name_of_columns(self, file_name):
        self.validation_logger.enter_into_method(inspect.stack()[0][3])

        values_from_schema = self.schema.get_values_from_schema()
        _csv = pd.read_csv(self.good_raw_folder + file_name)
        list_of_columns = list(_csv.columns)
        for i, name_of_column in enumerate(values_from_schema[2].keys()):
            if list_of_columns[i] != name_of_column:
                move(self.good_raw_folder + file_name, self.bad_raw_folder)
                log_message = f'Invalid name of column: {list_of_columns[i]} ' \
                              f'for the file: {file_name}, ' \
                              f'moved to {self.bad_raw_folder}'
                self.validation_logger.write_message_from_method(log_message)
        log_message = "check_file_for_wrong_name_of_columns completed!"
        self.validation_logger.write_message_from_method(log_message)
        self.validation_logger.exited_from_method(inspect.stack()[0][3])



