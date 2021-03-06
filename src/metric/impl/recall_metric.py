from metric import AbstractMetric
from sklearn.metrics import recall_score
from util import round_


class RecallMetric(AbstractMetric):
    def __init__(self, decimals=4, average='macro', rating_decimals=0):
        name = f'Recall'
        if average != 'macro':
            name += f'({average})'
 
        super().__init__(name, decimals)
        self._average = average
        self._rating_decimals = rating_decimals

    def _calculate(self, pred_values, true_values, ctx):
        true_values = [round_(v, self._rating_decimals) for v in true_values]
        pred_values = [round_(v, self._rating_decimals) for v in pred_values]

        return recall_score(true_values, pred_values, average=self._average, zero_division=0)
