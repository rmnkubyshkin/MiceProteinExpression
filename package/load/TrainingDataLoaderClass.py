from package.load.DataLoaderClass import DataLoader
from package.logging.LoggerPathsConstantClass import data_loader_for_training_logs
from package.logging.LoggingClass import Logger
from package.utils.FolderConstantsClass import training_input_filename, training_database_folder


class TrainingDataLoader(DataLoader):

    def __init__(self):
        self.training_data_load_logger = Logger(data_loader_for_training_logs)
        self.training_file = training_database_folder + training_input_filename
        super().__init__(self.training_data_load_logger)

    def read_data_from_csv(self):
        return super().read_data_from_csv(self.training_file)
