from package.validation.ValidationForTrainingClass import ValidationForTraining


def main():
    path = 'datafiles/training/raw_data/Data_Cortex_Nuclear_#1.xls'
    validation_object = ValidationForTraining(path)
    validation_object.convert_xls_to_csv()
    validation_object.validate_num_of_columns()
    validation_object.validate_file_name()
    validation_object.validate_missing_all_column_values_in_folder()
    validation_object.validate_name_of_columns()


if __name__ == "__main__":
    main()
