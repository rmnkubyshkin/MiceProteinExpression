import logging


class Logging:

    def __init__(self, log_type):
        log_type = "logs/training/validation/validation_for_training_logs.txt"
        format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename=log_type, level=logging.INFO, format=format, filemode='w')

    def write_message_from_method(self, message):
        logging.info(f'{message}')

    def enter_into_method(self, method_name):
        logging.info(f'Enter into method: {method_name}')

    def exited_from_method(self, method_name):
        logging.info(f'Exited from method: {method_name}')

    def exception(self, message, e):
        logging.exception(f'{message} : {e}')


