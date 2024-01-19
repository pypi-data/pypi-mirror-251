from mysticML.utils import Daddy
import pandas
pandas.options.mode.chained_assignment=None

class Duplicate(Daddy):
    """
        This class must run before data scaling (up-sampling).
    """
    def __init__(self, x:pandas.DataFrame, target:str=None, **kwargs) ->None:
        super().__init__(x, target, **kwargs)
        self.x = pandas.concat([self.x,self.y],axis=1)

    def check(self) ->bool:
        if not self.duplicate:
            return False
        return True

    def apply(self) ->pandas.DataFrame:
        if not self.check():
            return self.x
        in_size = len(self.x)
        self.x.drop_duplicates(inplace=True)
        if len(self.x) != in_size:
            self.report_.append("Duplicate")
        return self.x