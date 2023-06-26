from package.logging.LoggingClass import Logger
from package.transform.TransformationClass import Transformation
from package.logging.LoggerPathsConstantClass import transformation_for_prediction_logs
from package.utils.FolderConstantsClass import \
    prediction_validated_good_raw_data_folder, \
    prediction_transformed_data_folder


class TransformationForPrediction(Transformation):
    def __init__(self):
        self.transformation_logger = Logger(transformation_for_prediction_logs)
        self.good_raw_data_folder = prediction_validated_good_raw_data_folder
        self.transformed_data_folder = prediction_transformed_data_folder
        super().__init__(self.transformation_logger, self.good_raw_data_folder, self.transformed_data_folder)

    def impute_values(self):
        super().impute_values()

    def encode_class_column(self):
        super().encode_class_column()


