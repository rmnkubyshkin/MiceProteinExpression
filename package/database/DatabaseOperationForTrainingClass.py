from package.database.DatabaseOperationClass import DatabaseOperation
from package.logging.LoggerPathsConstantClass import database_operations_for_training_logs
from package.logging.LoggingClass import Logger
from package.utils.FolderConstantsClass import \
    training_transformed_data_folder, \
    training_validated_bad_raw_data_folder, \
    training_database_folder


class DataBaseOperationForTraining(DatabaseOperation):

    def __init__(self):
        self.db_operation_logs = Logger(database_operations_for_training_logs)
        self.transformed_folder = training_transformed_data_folder
        self.bad_raw_folder = training_validated_bad_raw_data_folder
        self.database_folder = training_database_folder
        self.database_name = "Training"
        super().__init__(self.db_operation_logs,
                         self.transformed_folder,
                         self.bad_raw_folder,
                         self.database_folder,
                         self.database_name
                         )

    def database_connection(self, database_name):
        return super().database_connection(database_name)

    def create_table_in_database(self):
        return super().create_table_in_database()

    def insert_data_in_database(self):
        return super().insert_data_in_database()
