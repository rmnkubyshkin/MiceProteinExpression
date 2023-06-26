import inspect
import pandas as pd
from warnings import simplefilter
from package.load.PredictionDataLoaderClass import PredictionDataLoader
from package.logging.LoggerPathsConstantClass import general_logs
from package.logging.LoggingClass import Logger
from package.model.ModelFinder import ModelFinder
from package.preprocess.ClusteringClass import KMeansClustering
from package.preprocess.PredictionPreprocessingClass import PredictionPreprocessing
from package.transform.TransformationForPredictionClass import TransformationForPrediction
from package.utils.FileOperationClass import FileOperation
from package.utils.FolderConstantsClass import output_prediction_file
from package.validate.ValidationForPredictionClass import ValidationForPrediction
from package.database.DatabaseOperationForPredictionClass import DataBaseOperationForPrediction


class Prediction:
    def __init__(self):
        self.predict_logger = Logger(general_logs)
        self.utils = FileOperation()
        self.validation = ValidationForPrediction()

    def predict(self):
        simplefilter(action='ignore', category=FutureWarning)
        try:
            self.predict_logger.enter_into_method(inspect.stack()[0][3])

            self.__validate_data__()

            self.__transform_data__()

            self.__aggregate_data_into_database__()

            self.__load_data_from_database__()

            preprocessor = PredictionPreprocessing()

            columns_to_drop = preprocessor.get_columns_with_zero_std_deviation(preprocessor.data)
            data = preprocessor.remove_columns_from_data(columns_to_drop)
            file_loader = FileOperation()
            k_means = file_loader.load_model('KMeans')

            clusters = k_means.predict(data.drop(['class_encoded'], axis=1))
            data['clusters'] = clusters
            clusters = data['clusters'].unique()
            result = []
            for i in clusters:
                cluster_data = data[data['clusters'] == i]
                encoded_classes = list(cluster_data['class_encoded'])
                cluster_data = data.drop(labels=['class_encoded'], axis=1)
                cluster_data = cluster_data.drop(['clusters'], axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                result = list(model.predict(cluster_data))
                result = pd.DataFrame(list(zip(encoded_classes, result)),
                                      columns=['encoded_classes', 'Prediction'])
                result.to_csv(output_prediction_file,
                              header=True,
                              mode='a+')
                log_message = 'End of prediction'
                self.predict_logger.write_message_from_method(log_message)
                self.predict_logger.exited_from_method(inspect.stack()[0][3])

        except Exception as e:
            log_message = f'Error occurred while running the prediction, Error {e}'
            self.predict_logger.exception(log_message, e)
            raise e

        return output_prediction_file, result.head().to_json(orient='records')

    def __validate_data__(self):
        self.validation.convert_xls_to_csv()
        self.validation.validate_num_of_columns()
        self.validation.validate_file_name()
        self.validation.validate_missing_all_column_values_in_folder()
        self.validation.validate_name_of_columns()

    def __transform_data__(self):
        self.transformation = TransformationForPrediction()
        self.transformation.encode_class_column()
        self.transformation.impute_values()

    def __aggregate_data_into_database__(self):
        self.database_operation = DataBaseOperationForPrediction()
        self.database_operation.create_table_in_database()
        self.database_operation.insert_data_in_database()
        self.database_operation.write_data_into_csv()

    def __load_data_from_database__(self):
        self.loader = PredictionDataLoader()
        self.loader.read_data_from_csv()


pred = Prediction()
pred.predict()
