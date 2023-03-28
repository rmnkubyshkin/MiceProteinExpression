import inspect
import pandas as pd


class DataLoader:

    def __init__(self, logger):
        self.data = []
        self.load_logger = logger

    def read_data_from_csv(self, file):
        self.load_logger.enter_into_method(inspect.stack()[0][3])

        try:
            self.data = pd.read_csv(file)

            log_message = "Data load successful"
            self.load_logger.write_message_from_method(log_message)
            self.load_logger.exited_from_method(inspect.stack()[0][3])
            return self.data
        except Exception as e:
            log_message = f'Exception occurred in read_from_csv method of the DataLoader class.' \
                          f'Exception message: {e}'
            self.load_logger.exception(log_message, e)
            log_message = f'DataLoader Unsuccessful.' \
                          f'Exited the {inspect.stack()[0][3]} method of the DataLoader class'
            self.load_logger.exception(log_message, e)
            raise e
