import inspect
from os import listdir

from package.logging.LoggingClass import Logging
from package.validation.ValidationClass import Validation
from package.utils import FolderConstantsClass as folder
from package.logging.LoggerPathsConstantClass import validation_for_training_logs
from package.utils.FolderConstantsClass import \
    training_validated_good_raw_data_folder,\
    training_validated_bad_raw_data_folder,\
    training_raw_data_folder,\
    training_converted_raw_data_folder


class ValidationForTraining(Validation):

    def __init__(self, dataset_path):
        self.logger = Logging(validation_for_training_logs)
        self.schema_path = "schemas/schema_training.json"
        self.good_raw_data_folder = training_validated_good_raw_data_folder
        self.bad_raw_data_folder = training_validated_bad_raw_data_folder
        self.batch_folder = training_raw_data_folder
        self.converted_folder = training_converted_raw_data_folder
        super().__init__(
            self.logger,
            self.schema_path,
            self.batch_folder,
            self.converted_folder,
            self.bad_raw_data_folder,
            self.good_raw_data_folder
        )

    def get_raw_data_folder(self):
        return self.raw_data_folder

    def create_manual_regex(self):
        pass

    def validate_mouse_id(self):
        pass

    def create_directory_for_validated_good_raw_data(self):
        pass

    def create_good_raw_data_folder(self):
        super().create_good_raw_data_folder(folder.training_validated_good_raw_data_folder)

    def create_bad_raw_data_folder(self):
        super().create_bad_raw_data_folder(folder.training_validated_bad_raw_data_folder)

    def delete_existing_good_raw_data_folder(self):
        super().delete_existing_good_raw_data_folder(folder.training_validated_good_raw_data_folder)

    def delete_existing_bad_raw_data_folder(self):
        super().delete_existing_bad_raw_data_folder(folder.training_validated_bad_raw_data_folder)

    def get_values_from_schema(self):
        log_file_path = "logs/training/validation/validation_for_training_logs.txt"
        super().get_values_from_schema(log_file_path)

    def validate_num_of_columns(self, num_of_columns):
        pass

