from package.validate.ValidationForTrainingClass import ValidationForTraining
from package.transform.TransformationForTrainingClass import TransformationForTraining
from package.database.DatabaseOperationForTrainingClass import DataBaseOperationForTraining
from MainPredictionClass import MainPrediction


def main():
    validation = ValidationForTraining()
    transformation = TransformationForTraining()
    database_operation = DataBaseOperationForTraining()

    validation.convert_xls_to_csv()
    validation.validate_num_of_columns()
    validation.validate_file_name()
    validation.validate_missing_all_column_values_in_folder()
    validation.validate_name_of_columns()

    transformation.encode_class_column()
    transformation.impute_values()
    database_operation.create_table_in_database()
    database_operation.insert_data_in_database()


if __name__ == "__main__":
    main()
