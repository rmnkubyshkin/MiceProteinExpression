import inspect

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

from package.logging.LoggerPathsConstantClass import model_finder_logs
from package.logging.LoggingClass import Logger


class ModelFinder:

    def __init__(self):
        self.model_logger = Logger(model_finder_logs)
        self.random_forest = RandomForestClassifier()
        self.kn_neighbors = KNeighborsClassifier()


    def dummy_best_params_for_random_forest(self, train_x, train_y):
        try:
            self.model_logger.enter_into_method(inspect.stack()[0][3])
            self.criterion, self.max_depth , self.max_features, self.n_estimators = ['entropy', 3, 'auto', 100]
            self.random_forest = RandomForestClassifier(
                n_estimators=self.n_estimators,
                criterion=self.criterion,
                max_depth=self.max_depth,
                max_features=self.max_features
            )
            self.random_forest.fit(train_x, train_y)
            self.model_logger.exited_from_method(inspect.stack()[0][3])
            return self.random_forest

        except Exception as e:
            log_message = f'Exception occurred in get_best_params_for_random_forest method of the ModelFinder class.' \
                          f'Exception message: {e}'
            self.model_logger.exception(log_message, e)
            raise Exception()
    def dummy_best_params_for_knn(self, train_x, train_y):

        try:
            self.algorithm, self.leaf_size, self.n_neighbors, self.p = ['ball_tree', 10, 4, 1]

            self.kn_neighbors = KNeighborsClassifier(
                algorithm=self.algorithm,
                leaf_size=self.leaf_size,
                n_neighbors=self.n_neighbors,
                p=self.p,
                n_jobs=-1
            )

            self.kn_neighbors.fit(train_x, train_y)
            return self.kn_neighbors

        except Exception as e:
            log_message = f'Exception occurred in knn method of the ModelFinder class. Exception message: {e}'
            self.model_logger.exception(log_message, e)
            self.model_logger.exited_from_method(inspect.stack()[0][3])
        raise e

    def get_best_params_for_random_forest(self, train_x, train_y):
        self.model_logger.enter_into_method(inspect.stack()[0][3])

        try:
            self.params_grid = {
                "n_estimators": [10, 50, 100, 130],
                "criterion": ['gini', 'entropy'],
                "max_depth": range(2, 4, 1),
                "max_features": ['auto', 'log2']
            }

            self.grid_search_cv = GridSearchCV(
                estimator=self.random_forest,
                param_grid=self.params_grid,
                verbose=3,
                cv=5
            )
            self.grid_search_cv.fit(train_x, train_y)

            self.criterion = self.grid_search_cv.best_params_['criterion']
            self.max_depth = self.grid_search_cv.best_params_['max_depth']
            self.max_features = self.grid_search_cv.best_params_['max_features']
            self.n_estimators = self.grid_search_cv.best_params_['n_estimators']

            self.random_forest = RandomForestClassifier(
                n_estimators=self.n_estimators,
                criterion=self.criterion,
                max_depth=self.max_depth,
                max_features=self.max_features
            )

            self.random_forest.fit(train_x, train_y)
            log_message = f'Random Forest best params: {self.grid_search_cv.best_params_}'
            self.model_logger.write_message_from_method(log_message)
            self.model_logger.exited_from_method(inspect.stack()[0][3])
            return self.random_forest

        except Exception as e:
            log_message = f'Exception occurred in get_best_params_for_random_forest method of the ModelFinder class.' \
                          f'Exception message: {e}'
            self.model_logger.exception(log_message, e)
            raise Exception()

    def get_best_params_for_knn(self, train_x, train_y):
        self.model_logger.enter_into_method(inspect.stack()[0][3])

        try:
            self.params_grid_knn = {
                'algorithm': ['ball_tree', 'kd_tree', 'brute'],
                'leaf_size': [10, 17, 24, 28, 30, 35],
                'n_neighbors': [4, 5, 8, 10, 11],
                'p': [1, 2]
            }

            self.grid_search_cv = GridSearchCV(
                self.kn_neighbors,
                self.params_grid_knn,
                verbose=3,
                cv=5
             )
            self.grid_search_cv.fit(train_x, train_y)

            self.algorithm = self.grid_search_cv.best_params_['algorithm']
            self.leaf_size = self.grid_search_cv.best_params_['leaf_size']
            self.n_neighbors = self.grid_search_cv.best_params_['n_neighbors']
            self.p = self.grid_search_cv.best_params_['p']

            self.kn_neighbors = KNeighborsClassifier(
                algorithm=self.algorithm,
                leaf_size=self.leaf_size,
                n_neighbors=self.n_neighbors,
                p=self.p,
                n_jobs=-1
            )


            self.kn_neighbors.fit(train_x, train_y)
            log_message = f'KNN best params: {self.grid_search_cv.best_params_}'
            self.model_logger.write_message_from_method(log_message)
            return self.kn_neighbors
        except Exception as e:
            log_message = f'Exception occurred in knn method of the ModelFinder class. Exception message: {e}'
            self.model_logger.exception(log_message, e)
            self.model_logger.exited_from_method(inspect.stack()[0][3])
            raise e

    def get_best_model(self, train_x, train_y, test_x, test_y):
        self.model_logger.enter_into_method(inspect.stack()[0][3])

        try:
            self.kn_neighbors = self.dummy_best_params_for_knn(train_x, train_y)
            self.prediction_of_knn = self.kn_neighbors.predict_proba(test_x)
            self.knn_score = self.get_score_of_prediction_model_name_with_label(
                self.prediction_of_knn,
                "KNNeighbors",
                test_y
            )

            self.random_forest = self.dummy_best_params_for_random_forest(train_x, train_y)
            self.prediction_of_random_forest = self.random_forest.predict_proba(test_x)
            self.random_forest_score = self.get_score_of_prediction_model_name_with_label(
                self.prediction_of_random_forest,
                "RandomForest",
                test_y
            )

            if self.random_forest_score < self.knn_score:
                return 'KNNeighbors', self.kn_neighbors
            else:
                return 'RandomForest', self.random_forest

        except Exception as e:
            log_message = f'Exception occurred in get_best_model method of the ModelFinder class. ' \
                          f'Exception message:{e}'
            self.model_logger.exception(log_message, e)
            self.model_logger.exited_from_method(inspect.stack()[0][3])
            raise e

    def get_score_of_prediction_model_name_with_label(self, prediction, model_name, test_y):
        if len(test_y.unique()) == 1:
            score = accuracy_score(test_y, prediction, multi_class='ovr')
            log_message = f'Accuracy for {model_name}: {score}'
            self.model_logger.write_message_from_method(log_message)
        else:
            score = roc_auc_score(test_y, prediction, multi_class='ovr')
            log_message = f'AUC for {model_name}: {score}'
            self.model_logger.write_message_from_method(log_message)
        return score
