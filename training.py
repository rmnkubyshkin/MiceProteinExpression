from sklearn.model_selection import train_test_split

from package.logging.LoggingClass import Logger
from package.model.ModelFinder import ModelFinder
from package.preprocess.ClusteringClass import KMeansClustering
from package.utils.FileOperationClass import FileOperation
from package.validate.ValidationForTrainingClass import ValidationForTraining
from package.transform.TransformationForTrainingClass import TransformationForTraining
from package.database.DatabaseOperationForTrainingClass import DataBaseOperationForTraining
from package.load.TrainingDataLoaderClass import TrainingDataLoader
from package.preprocess.TrainingPreprocessingClass import TrainingPreprocessing
from package.logging.LoggerPathsConstantClass import general_logs
import inspect


class Training:
    def __init__(self):
        self.train_logger = Logger(general_logs)
        self.utils = FileOperation()
        self.validation = ValidationForTraining()

    def train(self):
        try:
            self.train_logger.enter_into_method(inspect.stack()[0][3])

            self.__validate_data__()

            self.__transform_data__()

            self.__aggregate_data_into_database__()

            self.__load_data_from_database__()

            X, y = self.__preprocessing_data__()
            num_of_columns = self.cluster.find_optimum_num_of_clusters(X)
            self.cluster.create_clusters(X, num_of_columns)
            X['Labels'] = y
            list_of_clusters = X['Cluster'].unique()
            self.__save_best_models__(X, list_of_clusters)

            self.train_logger.exited_from_method(inspect.stack()[0][3])
        except Exception as e:
            self.train_logger.exception('Unsuccessful end of training!', e)
            raise e

    def __save_best_models__(self, X, list_of_clusters):
        for i in list_of_clusters:
            x_test, x_train, y_test, y_train = self.__train_split_data_for_each_clusters__(X, i)
            best_model_name, best_model = self.model_finder.get_best_model(x_train, y_train, x_test, y_test)
            self.utils.save_model(best_model, f'{best_model_name} - {i}')
            self.train_logger.write_message_from_method('Successful end of training!')

    def __train_split_data_for_each_clusters__(self, X, i):
        cluster_data = X[X['Cluster'] == i]
        cluster_features = cluster_data.drop(['Labels', 'Cluster'], axis=1)
        cluster_label = cluster_data['Labels']
        x_train, x_test, y_train, y_test = train_test_split(
            cluster_features,
            cluster_label,
            test_size=1 / 3,
            random_state=355
        )
        return x_test, x_train, y_test, y_train

    def __preprocessing_data__(self):
        self.preprocessor = TrainingPreprocessing()
        self.model_finder = ModelFinder()
        self.cluster = KMeansClustering()
        X, y = self.preprocessor.split_features_and_label()
        zero_mean_columns = self.preprocessor.get_columns_with_zero_std_deviation(X)
        if zero_mean_columns == 0:
            X = self.preprocessor.remove_columns_from_data(zero_mean_columns)
        return X, y

    def __load_data_from_database__(self):
        self.loader = TrainingDataLoader()
        self.loader.read_data_from_csv()

    def __aggregate_data_into_database__(self):
        self.database_operation = DataBaseOperationForTraining()
        self.database_operation.create_table_in_database()
        self.database_operation.insert_data_in_database()
        self.database_operation.write_data_into_csv()

    def __transform_data__(self):
        self.transformation = TransformationForTraining()
        self.transformation.encode_class_column()
        self.transformation.impute_values()

    def __validate_data__(self):
        self.validation.convert_xls_to_csv()
        self.validation.validate_num_of_columns()
        self.validation.validate_file_name()
        self.validation.validate_missing_all_column_values_in_folder()
        self.validation.validate_name_of_columns()


tr = Training()
tr.train()