import inspect
import os
import shutil
from os.path import isdir

from pickle4 import pickle

from package.logging.LoggerPathsConstantClass import file_operation_logs
from package.logging.LoggingClass import Logger
from package.utils.FolderConstantsClass import model_folder


class FileOperation:

    def __init__(self):
        self.file_operation_logger = Logger(file_operation_logs)
        self.model_folder = model_folder

    def save_model(self, model, filename):
        self.file_operation_logger.enter_into_method(inspect.stack()[0][3])

        try:
            path = os.path.join(self.model_folder, filename)
            if os.path.isdir(path):
                shutil.rmtree(self.model_folder)
            os.makedirs(path)

            with open(f'{path}/{filename}.sav', 'wb') as f:
                pickle.dump(model, f)

                log_message = f'Model File {filename} saved.'
                self.file_operation_logger.write_message_from_method(log_message)
                self.file_operation_logger.exited_from_method(inspect.stack()[0][3])
                return 'success'

        except Exception as e:
            log_message = f'Exception occurred in save_model method of the ModelFinder class. ' \
                          f'Exception message: {e}'
            self.file_operation_logger.exception(log_message, e)
            self.file_operation_logger.exited_from_method(inspect.stack()[0][3])
            raise e

    def load_model(self, filename):
        log_message = 'Entered the load_model method of the FileOperation class'
        self.file_operation_logger.write_message_from_method(log_message)
        try:
            full_file_name = f'{self.model_folder}{filename}/{filename}.sav'
            with open(full_file_name, 'rb') as f:
                log_message = f'Model File  {filename} loaded. '\
                              f'Exited the load_model method of the ModelFinder class'
                self.file_operation_logger.write_message_from_method(log_message)
                return pickle.load(f)

        except Exception as e:
            log_message = f'Exception occurred in load_model method of the ModelFinder class.' \
                          f'Exception message: {e}'
            self.file_operation_logger.write_message_from_method(log_message)
            raise Exception()

    def create_data_folder(self, data_folder):
        try:
            self.file_operation_logger.enter_into_method(inspect.stack()[0][3])

            self.__create_directory_if_not_exist(data_folder)

            self.file_operation_logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error while creating directory {e}'
            self.file_operation_logger.exception(log_message, e)
            raise e

    def find_correct_model_file(self, cluster_number):
        self.file_operation_logger.enter_into_method(inspect.stack()[0][3])

        try:
            self.cluster_number = cluster_number
            self.list_of_files = os.listdir(self.model_folder)
            for self.file in self.list_of_files:
                try:
                    if self.file.index(str(self.cluster_number)) != -1:
                        self.model_name = self.file
                except (Exception,):
                    continue

                self.model_name = self.model_name.split('.')[0]

                self.file_operation_logger.exited_from_method(inspect.stack()[0][3])
                return self.model_name

        except (Exception,) as e:
            log_message = 'Exception occurred in find_correct_model_file method of the ModelFinder class. ' \
                          'Exception message:  ' + str(e)
            self.file_operation_logger.exception(log_message, e)
            log_message = 'Exited the find_correct_model_file method of the ModelFinder class with Failure'
            self.file_operation_logger.exited_from_method(log_message)
            raise e

    def __create_directory_if_not_exist(self, data_folder):
        self.file_operation_logger.enter_into_method(inspect.stack()[0][3])

        if not isdir(data_folder):
            os.makedirs(data_folder)
            self.file_operation_logger.write_message_from_method(f'Folder: {data_folder} create successful!')

        self.file_operation_logger.exited_from_method(inspect.stack()[0][3])

    def delete_existing_data_folder(self, data_folder):
        try:
            self.file_operation_logger.enter_into_method(inspect.stack()[0][3])

            self._delete_directory_if_exist(data_folder)

            self.file_operation_logger.exited_from_method(inspect.stack()[0][3])
        except OSError as e:
            log_message = f'Error while creating directory {e}'
            self.file_operation_logger.exception(log_message, e)
            raise e

    def _delete_directory_if_exist(self, data_folder):
        self.file_operation_logger.enter_into_method(inspect.stack()[0][3])

        if isdir(data_folder):
            shutil.rmtree(data_folder)
            self.file_operation_logger.write_message_from_method(f'Folder: {data_folder} delete successful!')

        self.file_operation_logger.exited_from_method(inspect.stack()[0][3])
