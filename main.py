from package.utils.FileOperationClass import FileOperation
from package.validate.ValidationForTrainingClass import ValidationForTraining
from package.transform.TransformationForTrainingClass import TransformationForTraining
from package.database.DatabaseOperationForTrainingClass import DataBaseOperationForTraining
from package.load.TrainingDataLoaderClass import TrainingDataLoader
from package.preprocess.PreprocessingClass import Preprocessing

def main():
    validation = ValidationForTraining()
    transformation = TransformationForTraining()
    database_operation = DataBaseOperationForTraining()
    loader = TrainingDataLoader()
    preprocessor = Preprocessing()
    utils = FileOperation()

    validation.convert_xls_to_csv()
    validation.validate_num_of_columns()
    validation.validate_file_name()
    validation.validate_missing_all_column_values_in_folder()
    validation.validate_name_of_columns()

    transformation.encode_class_column()
    transformation.impute_values()
    database_operation.create_table_in_database()
    database_operation.insert_data_in_database()
    database_operation.write_data_into_csv()
    loader.read_data_from_csv()

    X, y = preprocessor.split_features_and_label()
    zero_mean_columns = preprocessor.get_columns_with_zero_std_deviation(X)
    if zero_mean_columns == 0:
        X = preprocessor.remove_columns_from_data(zero_mean_columns)
    model = []
    utils.save_model(model, "model")
    model = utils.load_model("model")


if __name__ == "__main__":
    main()
