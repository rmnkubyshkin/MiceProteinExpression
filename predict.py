from package.logging.LoggerPathsConstantClass import general_logs
from package.logging.LoggingClass import Logger
from package.utils.FileOperationClass import FileOperation
from package.validate.ValidationForTrainingClass import ValidationForTraining


class Predict:
    def __init__(self):
        self.predict_logger = Logger(general_logs)
        self.utils = FileOperation()
        self.validation = ValidationForTraining()

    def predict(self):
        pass
