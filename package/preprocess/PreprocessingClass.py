import inspect
import pandas as pd

from package.logging.LoggerPathsConstantClass import data_preprocess_logs
from package.logging.LoggingClass import Logger
from package.utils.FolderConstantsClass import training_input_filename, training_database_folder


class Preprocessing:

    def __init__(self):
        self.preprocess_logger = Logger(data_preprocess_logs)
        self.data = pd.read_csv(training_database_folder + training_input_filename)

    def split_features_and_label(self):
        self.preprocess_logger.enter_into_method(inspect.stack()[0][3])

        try:
            self.X = self.data.drop(labels='class_encoded', axis=1)
            self.y = self.data['class_encoded']

            log_message = f'Label Separation Successful!'
            self.preprocess_logger.write_message_from_method(log_message)
            self.preprocess_logger.exited_from_method(inspect.stack()[0][3])
            return self.X, self.y
        except Exception as e:
            log_message = f'Exception occurred in separate_label_feature method of the Preprocessing class.' \
                          f'Exception message: {e}'
            self.preprocess_logger.exception(log_message, e)
            log_message = f'Label Separation Unsuccessful. ' \
                          f'Exited the separate_label_feature method of the Preprocessing class'
            self.preprocess_logger.exception(log_message, e)
            raise e

    def get_columns_with_zero_std_deviation(self, columns):
        self.preprocess_logger.enter_into_method(inspect.stack()[0][3])
        self.columns = columns
        self.columns_to_drop = []

        try:
            self.get_one_column_with_std_deviation()

            log_message = "Column search for Standard Deviation of Zero Successful." \
                          "Exited the get_columns_with_zero_std_deviation method of the Preprocessing class"
            self.preprocess_logger.write_message_from_method(log_message)
            return self.columns_to_drop

        except Exception as e:
            log_message = f'Exception occurred in get_columns_with_zero_std_deviation method' \
                          f'of the Preprocessing class. Exception message: {e}' \
                          f'Exited the {inspect.stack()[0][3]} method of the Preprocessing class'
            self.preprocess_logger.exception(log_message, e)
            raise e

    def get_one_column_with_std_deviation(self):
        for x in self.columns:
            if self.data[x].std() == 0:
                self.columns_to_drop.append(x)

    def remove_columns_from_data(self, columns):
        self.preprocess_logger.enter_into_method(inspect.stack()[0][3])
        try:
            self.useful_data = self.data.drop(labels=columns, axis=1)
            log_message = 'Column removal successful. Exited the remove_columns method of the Preprocessing class'
            self.preprocess_logger.write_message_from_method(log_message)
            return self.useful_data

        except Exception as e:
            log_message = f'Exception occurred in remove_columns method of the Preprocessing class.' \
                          f'Exception message:{e}'
            self.preprocess_logger.exception(log_message, e)

            log_message = f'Column removal Unsuccessful.' \
                          f'Exited the remove_columns method of the Preprocessing class'
            self.preprocess_logger.write_log(log_message)
            raise e
