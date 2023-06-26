from package.load.DataLoaderClass import DataLoader
from package.logging.LoggerPathsConstantClass import data_loader_for_prediction_logs
from package.logging.LoggingClass import Logger
from package.utils.FolderConstantsClass import prediction_input_filename, prediction_database_folder


class PredictionDataLoader(DataLoader):

    def __init__(self):
        self.prediction_data_load_logger = Logger(data_loader_for_prediction_logs)
        self.prediction_file = prediction_database_folder + prediction_input_filename
        super().__init__(self.prediction_data_load_logger)

    def read_data_from_csv(self):
        return super().read_data_from_csv(self.prediction_file)
