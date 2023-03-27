from package.logging.LoggingClass import Logger
from package.transform.TransformationClass import Transformation
from package.logging.LoggerPathsConstantClass import transformation_for_training_logs
from package.utils.FolderConstantsClass import \
    training_validated_good_raw_data_folder, \
    training_transformed_data_folder


class TransformationForTraining(Transformation):
    def __init__(self):
        self.transformation_logger = Logger(transformation_for_training_logs)
        self.good_raw_data_folder = training_validated_good_raw_data_folder
        self.transformed_data_folder = training_transformed_data_folder
        super().__init__(self.transformation_logger, self.good_raw_data_folder, self.transformed_data_folder)

    def impute_values(self):
        super().impute_values()

    def encode_class_column(self):
        super().encode_class_column()


