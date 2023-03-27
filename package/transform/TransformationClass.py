import inspect
import json
import os
from os import listdir
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder

from MainPredictionClass import MainPrediction


class Transformation(MainPrediction):
    def __init__(self, logger, good_raw_data_folder, transformed_data_folder):
        self.logger = logger
        self.good_raw_data_folder = good_raw_data_folder
        self.transformed_data_folder = transformed_data_folder

    def encode_class_column(self):
        try:
            self.logger.enter_into_method(inspect.stack()[0][3])

            self._encode_class_column_in_folder(self.good_raw_data_folder)

            self.logger.exited_from_method(inspect.stack()[0][3])
        except Exception as e:
            log_message = f'Class column encoder failed because::{e}'
            self.logger.exception(log_message, e)
            raise e

    def impute_values(self):
        try:
            self.logger.enter_into_method(inspect.stack()[0][3])

            self._impute_values_in_folder(self.transformed_data_folder)

            self.logger.exited_from_method(inspect.stack()[0][3])
        except Exception as e:
            log_message = f'Data Transformation failed because::{e}'
            self.logger.exception(log_message, e)
            raise e

    def _encode_class_column_in_folder(self, good_raw_data_folder):
        self.create_folder(self.transformed_data_folder)

        only_files = [f for f in listdir(good_raw_data_folder)]
        for file in only_files:
            full_path_of_file = pd.read_csv(good_raw_data_folder + "/" + file)
            encoded_data = self._encode_class_column_in_file(full_path_of_file)
            encoded_data.to_csv(self.transformed_data_folder + "/" + file, index=None, header=True)
            log_message = f' {file} - File encoded successfully!'
            self.logger.write_message_from_method(log_message)

    def _encode_class_column_in_file(self, data):
        ordinal_encoder = OrdinalEncoder()
        class_numerical = data[['class']]
        class_encoded = ordinal_encoder.fit_transform(class_numerical)
        data = data.drop(['class'], axis=1)
        data['class_encoded'] = class_encoded
        return data

    def _drop_varchar_columns(self, data):
        numerical_data = data.drop(["MouseID", "Genotype", "Treatment", "Behavior"], axis=1)
        return numerical_data

    def _impute_values_in_folder(self, transformed_folder):
        only_files = [f for f in listdir(transformed_folder)]
        for file in only_files:
            full_path_of_file = pd.read_csv(transformed_folder + "/" + file)
            imputed_data = self._impute_values_in_file(full_path_of_file)
            imputed_data.to_csv(transformed_folder + "/" + file, index=None, header=True)
            log_message = f' {file} - File Transformed successfully!'
            self.logger.write_message_from_method(log_message)

    def _impute_values_in_file(self, data):
        imputer = SimpleImputer(strategy='median')
        data_num = self._drop_varchar_columns(data)
        imputer.fit(data_num)
        X = imputer.transform(data_num)
        data = pd.DataFrame(X, columns=data_num.columns, index=data_num.index)
        return data

    def create_folder(self, folder):
        try:
            self.logger.enter_into_method(inspect.stack()[0][3])

            if not os.path.exists(folder):
                os.makedirs(folder)

            self.logger.exited_from_method(inspect.stack()[0][3])
        except Exception as e:
            log_message = f'Error while creating database folder {folder}: {e}'
            self.logger.exception(log_message, e)
            raise e

