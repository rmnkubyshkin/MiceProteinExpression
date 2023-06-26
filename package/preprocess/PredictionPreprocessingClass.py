import pandas as pd

from package.logging.LoggerPathsConstantClass import data_preprocess_for_prediction_logs
from package.logging.LoggingClass import Logger
from package.preprocess.PreprocessingClass import Preprocessing
from package.utils.FolderConstantsClass import prediction_database_folder, prediction_input_filename


class PredictionPreprocessing(Preprocessing):

    def __init__(self):
        self.preprocess_logger = Logger(data_preprocess_for_prediction_logs)
        self.data = pd.read_csv(prediction_database_folder + prediction_input_filename)
        super().__init__(self.preprocess_logger, self.data)

    def split_features_and_label(self):
        return super().split_features_and_label()

    def get_columns_with_zero_std_deviation(self, columns):
        return super().get_columns_with_zero_std_deviation(columns)

    def remove_columns_from_data(self, columns):
        return super().remove_columns_from_data(columns)
