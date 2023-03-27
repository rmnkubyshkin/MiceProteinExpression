import csv
import inspect
import os
import shutil
import sqlite3
from os import listdir

from MainPredictionClass import MainPrediction
from package.schemas.TrainingSchemaOperationsClass import TrainingSchemaOperations


class DatabaseOperation(MainPrediction):

    def __init__(self,
                 logger,
                 transformed_folder,
                 bad_raw_folder,
                 database_folder,
                 database_name
                 ):
        self.database_logger = logger
        self.bad_raw_folder = bad_raw_folder
        self.transformed_folder = transformed_folder
        self.database_folder = database_folder
        self.database_name = database_name
        self.schema_training = TrainingSchemaOperations()

    def database_connection(self, database_name):
        try:
            self.database_logger.enter_into_method(inspect.stack()[0][3])

            self.create_folder(self.database_folder)
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

    def create_folder(self, folder):
        try:
            self.database_logger.enter_into_method(inspect.stack()[0][3])

            if not os.path.exists(folder):
                os.makedirs(folder)

            self.database_logger.exited_from_method(inspect.stack()[0][3])
        except Exception as e:
            log_message = f'Error while creating database folder {folder}: {e}'
            self.database_logger.exception(log_message, e)
            raise e

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
                log_message = f'Tables created successfully!'
                self.database_logger.write_message_from_method(log_message)
                log_message = f'Database: {self.database_name} closed successfully!'
                self.database_logger.write_message_from_method(log_message)
            else:
                for _key in column_names.keys():
                    _type = column_names[_key]
                    try:
                        database_connection.execute(
                            'ALTER TABLE transformed_data ADD COLUMN "{column_name}" {data_type}'
                            .format(column_name=_key, data_type=_type))
                    except (Exception,):
                        database_connection.execute(
                            'CREATE TABLE transformed_data ({column_name} {data_type})'
                            .format(column_name=_key, data_type=_type))

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
        only_files = [f for f in listdir(self.transformed_folder)]
        for file in only_files:
            try:
                with open(self.transformed_folder + '/' + file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                connection.execute('INSERT INTO transformed_data values (%s)' % list_)
                                connection.commit()

                            except Exception as e:
                                raise e
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

