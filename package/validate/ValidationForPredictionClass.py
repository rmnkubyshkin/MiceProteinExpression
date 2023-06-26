from package.logging.LoggingClass import Logger
from package.validate.ValidationClass import Validation
from package.logging.LoggerPathsConstantClass import validation_for_prediction_logs
from package.utils.FolderConstantsClass import \
    prediction_validated_good_raw_data_folder,\
    prediction_validated_bad_raw_data_folder,\
    prediction_raw_data_folder,\
    prediction_converted_raw_data_folder


class ValidationForPrediction(Validation):

    def __init__(self):
        self.validation_logger = Logger(validation_for_prediction_logs)
        self.good_raw_data_folder = prediction_validated_good_raw_data_folder
        self.bad_raw_data_folder = prediction_validated_bad_raw_data_folder
        self.batch_folder = prediction_raw_data_folder
        self.converted_folder = prediction_converted_raw_data_folder
        super().__init__(
            self.validation_logger,
            self.batch_folder,
            self.converted_folder,
            self.bad_raw_data_folder,
            self.good_raw_data_folder,
        )

    def validate_num_of_columns(self):
        super().validate_num_of_columns()

    def validate_file_name(self):
        super().validate_file_name()

    def validate_name_of_columns(self):
        super().validate_name_of_columns()
