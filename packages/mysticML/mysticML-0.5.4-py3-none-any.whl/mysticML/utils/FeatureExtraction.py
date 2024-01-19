from mysticML.utils import Daddy
import pandas
from sklearn.decomposition import PCA
from math import ceil
pandas.options.mode.chained_assignment=None

class FeatureExtraction(Daddy):

    def __init__(self,x:pandas.DataFrame, target:str=None, **kwargs)->None:
        super().__init__(x, target, **kwargs)
        self.pca = None
        self.s = None

    def check(self) ->bool:
        if not self.feature_ext:
            return False
        self.s = self.x.shape[1]
        if self.x.shape[0] < self.s:
            self.s = self.x.shape[0]
            self.pca = PCA(n_components=ceil(self.s/2))
            return True
        if self.s > 6:
            self.pca = PCA(n_components=ceil(self.s/2))
            return True
        return False

    def apply(self) ->pandas.DataFrame:
        if not self.check():
            return pandas.concat([self.x, self.y], axis=1)
        self.report_.append("FeatureExt")
        columns = ['pca_comp_%i' % i for i in range(ceil(self.s/2))]
        x = pandas.DataFrame(self.pca.fit(self.x).transform(self.x), columns=columns)
        return pandas.concat([x, self.y], axis=1)
