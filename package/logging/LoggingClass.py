import logging


class Logging:

    def __init__(self, log_type):
        self.log_type = log_type
        self.format = '%(asctime)s - %(levelname)s - %(message)s'

    def write_message_from_method(self, message):
        logging.basicConfig(filename=self.log_type, level=logging.INFO, format=self.format, filemode='w')
        logging.info(f'{message}')

    def enter_into_method(self, method_name):
        logging.basicConfig(filename=self.log_type, level=logging.INFO, format=self.format, filemode='w')
        logging.info(f'Enter into method: {method_name}')

    def exited_from_method(self, method_name):
        logging.basicConfig(filename=self.log_type, level=logging.INFO, format=self.format, filemode='w')
        logging.info(f'Exited from method: {method_name}')

    def exception(self, message, e):
        logging.basicConfig(filename=self.log_type, level=logging.ERROR, format=self.format, filemode='w')
        logging.exception(f'{message} : {e}')


