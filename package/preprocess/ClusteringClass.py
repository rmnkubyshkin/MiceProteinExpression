import inspect

from kneed import KneeLocator
from sklearn.cluster import KMeans
from package.logging.LoggerPathsConstantClass import data_clustering_logs
from package.logging.LoggingClass import Logger
from package.utils.FileOperationClass import FileOperation
import matplotlib.pyplot as plt


class KMeansClustering:

    def __init__(self):
        self.clustering_logs = Logger(data_clustering_logs)

    def find_optimum_num_of_clusters(self, data):
        self.clustering_logs.enter_into_method(inspect.stack()[0][3])

        wcss = []
        try:
            for i in range(1, 11):
                k_means = KMeans(n_clusters=i, init='k-means++', random_state=42)
                k_means.fit(data)
                wcss.append(k_means.inertia_)
            plt.plot(range(1, 11), wcss)
            plt.title("The Elbow method")
            plt.xlabel("Number of clusters")
            plt.ylabel("WCSS")
            plt.savefig('datafiles/elbow.png')
            self.locator = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')

            log_message = f'The optimum number of clusters is: {self.locator.knee}'
            self.clustering_logs.write_message_from_method(log_message)
            self.clustering_logs.exited_from_method(inspect.stack()[0][3])
            return self.locator.knee

        except Exception as e:
            log_message = f'Exception occurred in find_optimum_num_of_clusters method of the KMeansClustering class.' \
                          f'Exception message:{e}'
            self.clustering_logs.exception(log_message, e)
            self.clustering_logs.exited_from_method(inspect.stack()[0][3])
            raise e

    def create_clusters(self, data, number_of_clusters):
        self.clustering_logs.enter_into_method(inspect.stack()[0][3])
        self.data = data
        try:
            self.k_means = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)
            self.cluster_of_k_means = self.k_means.fit_predict(self.data)
            self.file_operation = FileOperation()
            self.saved_model = self.file_operation.save_model(self.k_means, 'KMeans')
            self.data['Cluster'] = self.cluster_of_k_means
            log_message = f'Successfully created {self.locator.knee} clusters.'
            self.clustering_logs.write_message_from_method(log_message)
            self.clustering_logs.exited_from_method(inspect.stack()[0][3])
            return self.data

        except Exception as e:
            log_message = f'Exception occurred in create_clusters method of the KMeansClustering class. ' \
                          f'Fitting the data to clusters failed. Exception message: {e}'
            self.clustering_logs.exception(log_message, e)
            self.clustering_logs.exited_from_method(inspect.stack()[0][3])
            raise e