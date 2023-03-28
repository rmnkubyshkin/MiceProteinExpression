import inspect
import os
import shutil

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
            if os.path.isdir(self.model_folder):
                shutil.rmtree(self.model_folder)
            os.makedirs(self.model_folder)

            with open(f'{self.model_folder}/{filename}.sav', 'wb') as f:
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
            full_file_name = f'{self.model_folder}/{filename}.sav'
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
