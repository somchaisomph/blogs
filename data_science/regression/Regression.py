import numpy as np

class LinRegr():
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

#--------------------------------------------------------------------------------    

class SimpleRegr(LinRegr):
    def fit(self,X,Y):
        X = np.insert(X,0,1,axis=1) # inject X0 into input vector with value 1
        
        _beta = np.zeros(X.shape[1]) # create beta vector 
        for i in range(self.iteration):
            for x,y in zip(X,Y):
                output = x.dot(_beta)
                _error = y - output 
                _beta = _beta + self.learning_rate * _error * x
        self.beta = _beta
    
    def predict(self,X):
        if self.beta is not None :
            X = np.insert(X,0,1,axis=1) 
            res= X.dot(self.beta)
            return res.reshape((X.shape[0],1))
            
        else :
            return None        
        
    def r2(self,X,Y):
        '''
        r2 is defined by 1-u/v
        where 
        u = sum of (observ - predict)^2
        v = sum of (observ - mean of observ)^2
        '''
        u = np.sum(np.power(Y - self.predict(X) ,2))
        v = np.sum(np.power(Y - Y.mean(),2))
        return 1 - u/v
#--------------------------------------------------------------------------------    
class LogisticRegr(LinRegr):
    def fit(self,X,Y):
        X = np.insert(X,0,1,axis=1) # inject X0 into input vector 
		num_x = X.shape[0] # number of rows
		_beta = np.zeros((X.shape[1],1)) # create beta vector 
		for i in range(self.iteration):
			z = X.dot(_beta)
			h = self.sigmoid(z)
			e = Y - h
			g = np.dot(X.T,e)
			_beta += (self.learning_rate/num_x) * g
		self.beta = _beta
    
    def predict(self,X):
        if self.beta is not None :
            X = np.insert(X,0,1,axis=1) 
            res = self.sigmoid(X.dot(self.beta.T))
            res = np.where(res >= 0.5,1,0)
            return res.astype(int)
            
        else :
            return None
        
    def sigmoid(self,h):
        return 1/(1 + np.exp(-h))

#--------------------------------------------------------------------------------        
def test_simple_regr():
    
    X = np.array([[1],[2],[3],[4],[5]])
    Y = np.array([[1],[2],[3],[4],[5]])
    lr = SimpleRegr()
    lr.iteration = 1000
    lr.fit(X,Y)
    print(lr.beta)
    print(lr.predict(np.array([[7],[8],[100]])))
    print(lr.r2(X,Y))

def test_logistic():
    logr = LogisticRegr()
    logr.iteration = 1000
    X = np.array([[1,3],[3,5],[5,7]])
    Y = np.array([[1,0,0]])
    logr.fit(X,Y)
    print(logr.beta)
    print(logr.predict(np.array([[3,5]])))

if __name__ == "__main__":
    test_simple_regr()
    test_logistic()
