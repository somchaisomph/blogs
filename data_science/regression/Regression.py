class Regression():
    def __init__(self):
        self._iter = 1000
        self._lr = 0.1
        self._beta = None
    
    @property
    def iteration(self):
        return self._iter
    
    @property
    def learning_rate(self):
        return self._lr
    
    @property
    def beta(self):
        return self._beta    
    
    @iteration.setter
    def iteration(self,i):
        self._iter = i
        
    @learning_rate.setter
    def learning_rate(self,lr):
        self._lr = lr
    
    @beta.setter
    def beta(self,b):
        self._beta = b
    
    def fit(self,X,Y):
        pass
    
    def predict(self,X):
        pass
        
        
    def r2(self,X,Y):
        pass
    
