from package.database.DatabaseOperationClass import DatabaseOperation
from package.logging.LoggerPathsConstantClass import database_operations_for_prediction_logs
from package.logging.LoggingClass import Logger
from package.utils.FolderConstantsClass import \
    prediction_transformed_data_folder, \
    prediction_validated_bad_raw_data_folder, \
    prediction_database_folder, prediction_input_filename


class DataBaseOperationForPrediction(DatabaseOperation):

    def __init__(self):
        self.db_operation_logs = Logger(database_operations_for_prediction_logs)
        self.transformed_folder = prediction_transformed_data_folder
        self.bad_raw_folder = prediction_validated_bad_raw_data_folder
        self.database_folder = prediction_database_folder
        self.database_name = "Prediction"
        self.output_file = prediction_input_filename
        super().__init__(self.db_operation_logs,
                         self.transformed_folder,
                         self.bad_raw_folder,
                         self.database_folder,
                         self.database_name,
                         self.output_file
                         )

    def database_connection(self, database_name):
        return super().database_connection(database_name)

    def create_table_in_database(self):
        database_connection = self.database_connection(self.database_name)
        database_connection.execute('DROP TABLE IF EXISTS transformed_data;')

        return super().create_table_in_database(database_connection)

    def insert_data_in_database(self):
        return super().insert_data_in_database()

    def write_data_into_csv(self):
        return super().write_data_into_csv()
