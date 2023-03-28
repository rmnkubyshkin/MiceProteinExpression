import logging
import os
from package.logging.LoggerPathsConstantClass import general_logs


class Logger:

    def __init__(self, log_type):
        self.log_type = log_type
        folder_for_logs = self.log_type.rsplit('/', 1)[0]
        if not os.path.exists(folder_for_logs):
            os.makedirs(folder_for_logs)

        logging.basicConfig(level=logging.INFO, filemode="w", filename=general_logs,
                            format='%(asctime)s - %(levelname)s - %(message)s')

        self.file_handler = logging.FileHandler(str(self.log_type))
        self.format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.file_handler.setFormatter(self.format)

        self.logger = logging.getLogger(self.log_type)
        self.logger.addHandler(self.file_handler)

    def write_message_from_method(self, message):
        self.logger.setLevel(logging.INFO)
        self.logger.info(f'{message}')

    def enter_into_method(self, method_name):
        self.logger.setLevel(logging.INFO)
        self.logger.info(f'Enter into method: {method_name}')

    def exited_from_method(self, method_name):
        self.logger.setLevel(logging.INFO)
        self.logger.info(f'Exited from method: {method_name}')

    def exception(self, message, e):
        self.logger.setLevel(logging.ERROR)
        self.logger.exception(f'{message} : {e}')


