import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from sklearn.metrics import mean_squared_error
from math import sqrt


def metrics_fn(predictions, true_values, decimals=3):
    MSE = mean_squared_error(predictions, true_values)
    return { 'RMSE': round(sqrt(MSE), decimals),  'MSE': round(MSE, decimals) }


class AbstractPredictor(ABC):
    def __init__(self, rm, sim_service):
        self.sim_service = sim_service
        self.rm = rm

    @abstractmethod    
    def predict(self, user_id, item_id, decimals=0):
        pass

    def evaluate(self, rm, metrics_fn=metrics_fn, decimals=3):
        predictions = []
        true_values = []

        for _, user_id, item_id in rm.cells:
            true_value = rm.cell(user_id, item_id)
            if true_value > 0:
                predictions.append(self.predict(user_id, item_id, decimals))
                true_values.append(true_value)

        return metrics_fn(predictions, true_values, decimals)
