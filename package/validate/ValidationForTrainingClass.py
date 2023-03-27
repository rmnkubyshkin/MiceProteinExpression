from package.logging.LoggingClass import Logger
from package.validate.ValidationClass import Validation
from package.logging.LoggerPathsConstantClass import validation_for_training_logs
from package.utils.FolderConstantsClass import \
    training_validated_good_raw_data_folder,\
    training_validated_bad_raw_data_folder,\
    training_raw_data_folder,\
    training_converted_raw_data_folder


class ValidationForTraining(Validation):

    def __init__(self):
        self.validation_logger = Logger(validation_for_training_logs)
        self.good_raw_data_folder = training_validated_good_raw_data_folder
        self.bad_raw_data_folder = training_validated_bad_raw_data_folder
        self.batch_folder = training_raw_data_folder
        self.converted_folder = training_converted_raw_data_folder
        super().__init__(
            self.validation_logger,
            self.batch_folder,
            self.converted_folder,
            self.bad_raw_data_folder,
            self.good_raw_data_folder,
        )

    def create_good_raw_data_folder(self):
        super().create_good_raw_data_folder()

    def create_bad_raw_data_folder(self):
        super().create_bad_raw_data_folder()

    def delete_existing_good_raw_data_folder(self):
        super().delete_existing_good_raw_data_folder()

    def delete_existing_bad_raw_data_folder(self):
        super().delete_existing_bad_raw_data_folder()

    def delete_existing_converted_raw_data_folder(self):
        super().delete_existing_converted_raw_data_folder()

    def get_values_from_schema(self):
        return super().get_values_from_schema()

    def validate_num_of_columns(self):
        super().validate_num_of_columns()

    def validate_file_name(self):
        super().validate_file_name()

    def validate_name_of_columns(self):
        super().validate_name_of_columns()
