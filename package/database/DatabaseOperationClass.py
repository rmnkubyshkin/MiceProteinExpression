import csv
import inspect
import shutil
import sqlite3
from os import listdir


from package.schemas.TrainingSchemaOperationsClass import TrainingSchemaOperations
from package.utils.FileOperationClass import FileOperation
from package.utils.FolderConstantsClass import training_input_filename, training_database_folder


class DatabaseOperation:

    def __init__(self,
                 logger,
                 transformed_folder,
                 bad_raw_folder,
                 database_folder,
                 database_name,
                 ):
        self.database_logger = logger
        self.bad_raw_folder = bad_raw_folder
        self.transformed_folder = transformed_folder
        self.database_folder = database_folder
        self.database_name = database_name
        self.schema_training = TrainingSchemaOperations()
        self.file_operation = FileOperation()

    def database_connection(self, database_name):
        try:
            self.database_logger.enter_into_method(inspect.stack()[0][3])
            self.file_operation.create_data_folder(self.database_folder)

            database_connection = sqlite3.connect(self.database_folder + database_name + '.db')
            log_message = f'Opened {database_name} database successfully'
            self.database_logger.write_message_from_method(log_message)

            self.database_logger.exited_from_method(inspect.stack()[0][3])
        except ConnectionError as e:
            log_message = f'Error while connecting to database: {e}'
            self.database_logger.exception(log_message, e)
            raise e
        except Exception as e:
            log_message = f'Error in database_connection: {e}'
            self.database_logger.exception(log_message, e)
            raise e
        return database_connection

    def create_table_in_database(self):
        try:
            column_names = self.schema_training.get_values_from_schema()[0]
            database_connection = self.database_connection(self.database_name)
            cursor = database_connection.cursor()
            cursor.execute(
                "SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'transformed_data'"
            )

            if cursor.fetchone()[0] == 1:
                database_connection.close()
            else:
                self.__update_or_create_columns_in_table_with_connection(column_names, database_connection)
                database_connection.close()

            log_message = f'Tables created successfully!'
            self.database_logger.write_message_from_method(log_message)
            log_message = f'Database: {self.database_name} closed successfully!'
            self.database_logger.write_message_from_method(log_message)
        except Exception as e:
            log_message = f'Error while creating table:{e}'
            self.database_logger.exception(log_message, e)
            log_message = f'Database: {self.database_name} closed successfully!'
            self.database_logger.write_message_from_method(log_message)
            raise e

    def insert_data_in_database(self):
        self.database_logger.enter_into_method(inspect.stack()[0][3])

        connection = self.database_connection(self.database_name)
        files_directory = [f for f in listdir(self.transformed_folder)]
        for file in files_directory:
            self.__insert_data_from_file_with_connection(file, connection)

    def write_data_into_csv(self):
        try:
            self.database_logger.enter_into_method(inspect.stack()[0][3])
            self.output_file = training_input_filename
            connection = self.database_connection(self.database_name)
            sql_select = "SELECT * FROM transformed_data"
            cursor = connection.cursor()

            cursor.execute(sql_select)
            results = cursor.fetchall()
            headers = [i[0] for i in cursor.description]

            csv_file = csv.writer(open(self.database_folder + self.output_file, "w", newline=''),
                                  delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL,
                                  escapechar='\\')
            csv_file.writerow(headers)
            csv_file.writerows(results)

            log_message = "File exported successfully!"
            self.database_logger.write_message_from_method(log_message)
            self.database_logger.exited_from_method(inspect.stack()[0][3])
        except Exception as e:
            log_message = f'File exporting failed. Error : {e}'
            self.database_logger.exception(log_message, e)

    def __update_or_create_columns_in_table_with_connection(self, column_names, database_connection):
        for _key in column_names.keys():
            _type = column_names[_key]
            try:
                database_connection.execute(f'ALTER TABLE transformed_data ADD COLUMN "{_key}" {_type}')
            except (Exception,):
                database_connection.execute(f'CREATE TABLE transformed_data ({_key} {_type})')

    def __insert_data_from_file_with_connection(self, file, connection):
        try:
            with open(self.transformed_folder + '/' + file, "r") as f:
                next(f)
                reader = csv.reader(f, delimiter="\n")
                for column in enumerate(reader):
                    self.__insert_column_into_csv_with_connection(column, connection)
            log_message = f'{file}: File loaded successfully!'
            self.database_logger.write_message_from_method(log_message)
            self.database_logger.exited_from_method(inspect.stack()[0][3])
        except Exception as e:
            connection.rollback()
            log_message = f'Error while creating table: {e}'
            self.database_logger.exception(log_message, e)
            shutil.move(self.transformed_folder + '/' + file, self.bad_raw_folder)
            log_message = f'File: {file} moved successfully to {self.bad_raw_folder}'
            self.database_logger.write_message_from_method(log_message)
            connection.close()

    def __insert_column_into_csv_with_connection(self, column, connection):
        for _list in (column[1]):
            try:
                connection.execute('INSERT INTO transformed_data values (%s)' % _list)
                connection.commit()

            except Exception as e:
                raise e




