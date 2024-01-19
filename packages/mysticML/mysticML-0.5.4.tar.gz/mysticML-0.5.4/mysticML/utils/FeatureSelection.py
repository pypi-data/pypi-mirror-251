from mysticML.utils import Daddy
import pandas
import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest, f_classif, f_regression
pandas.options.mode.chained_assignment=None

class FeatureSelection(Daddy):
    def __init__(self, x:pandas.DataFrame, target:str=None,**kwargs)->None:
        super().__init__(x, target, **kwargs)
        self.app = None

    def check(self) ->bool:
        if not self.feature_sel:
            return False
        var = VarianceThreshold(threshold=0.0)
        try:
            var.fit(self.x)
            low_col = [column for column in self.x.columns
                       if column not in self.x.columns[var.get_support()]]
            self.x.drop(low_col, axis=1, inplace=True)
        except ValueError:
            # print('raised error by var.fit')
            pass
        s = self.x.shape[1]
        if s > 6:
            if self.y.nunique() > 0.0275*self.x.shape[0] and self.y.dtype != 'object':
                self.app = SelectKBest(score_func=f_regression, k=int(s/2))
            else:
                self.app = SelectKBest(score_func=f_classif, k=int(s/2))
            return True
        else:
            return False

    def apply(self) ->pandas.DataFrame:
        if not self.check():
            return pandas.concat([self.x,self.y],axis=1)
        # print(self.x.nunique())
        self.report_.append("FeatureSel")
        scores = self.app.fit(self.x,self.y).scores_
        average = np.average(scores)
        values = []
        compare = self.app.get_support(indices=True)
        for i in scores:
            if i>average:
                values.append(True)
            else:
                values.append(False)
        if values.count(True)<len(compare):
            self.x = self.x.iloc[:,compare]
        else:
            self.x = self.x.iloc[:,values]
        return pandas.concat([self.x, self.y], axis=1)
