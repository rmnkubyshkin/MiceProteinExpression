from package.validation.ValidationForTrainingClass import ValidationForTraining


def main():
    path = 'datafiles/training/raw_data/Data_Cortex_Nuclear_#1.xls'
    validation_object = ValidationForTraining(path)
    validation_object.delete_existing_good_raw_data_folder()
    validation_object.create_good_raw_data_folder()
    validation_object.delete_existing_bad_raw_data_folder()
    validation_object.create_bad_raw_data_folder()
    validation_object.get_values_from_schema()
    validation_object.convert_xls_to_csv()
    file_name, file_number, column_names, num_of_columns = validation_object.get_values_from_schema()
    validation_object.validate_num_of_columns(num_of_columns)


if __name__ == "__main__":
    main()
