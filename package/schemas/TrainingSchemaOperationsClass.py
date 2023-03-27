import inspect
import json

from package.logging.LoggerPathsConstantClass import schema_for_training_logs
from package.logging.LoggingClass import Logger
from package.schemas.SchemasOperationsClass import SchemaOperations


class TrainingSchemaOperations(SchemaOperations):

    def __init__(self):
        self.schema_logger = Logger(schema_for_training_logs)
        self.schema_path = "package/schemas/schema_training.json"

    def get_values_from_schema(self):
        self.schema_logger.enter_into_method(inspect.stack()[0][3])
        try:
            with open(self.schema_path, 'r') as f:
                dictionary = json.load(f)
                f.close()
            column_names = dictionary['column_names']
            num_of_columns = dictionary['num_of_columns']

            log_message = (
                           f'column_names:: {column_names},'
                           f'num_of_columns:: {num_of_columns}'
                           )
            self.schema_logger.write_message_from_method(log_message)
            self.schema_logger.exited_from_method(inspect.stack()[0][3])
        except ValueError as e:
            log_message = "ValueError: Value not found inside schema_validation.json"
            self.schema_logger.exception(log_message, e)
            raise e
        except KeyError as e:
            log_message = "KeyError: Key not found inside schema_validation.json"
            self.schema_logger.exception(log_message, e)
            raise e
        except Exception as e:
            self.schema_logger.exception("Exception", e)
            raise e

        return column_names, num_of_columns

