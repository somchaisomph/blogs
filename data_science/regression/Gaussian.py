import math

class Gaussian():
    def __init__(self,mean,var,size):
        '''
        Reference :
        https://en.m.wikipedia.org/wiki/Mixture_model
        https://math.stackexchange.com/questions/1112866/product-of-two-gaussian-pdfs-is-a-gaussain-pdf-but-product-of-two-gaussan-varia
        https://ccrma.stanford.edu/~jos/sasp/Product_Two_Gaussian_PDFs.html
        '''
        self._mean = mean
        self._var = var
        self._size = size

    def __add__(self,g):
        # g is another Gaussian with mean, varience
        # Gaussian + Gaussian 
        # mu = mu1 + mu2
        # var = var1 + var2
        m = self.mean() + g.mean()
        v = self.var() + g.var()
        return Gaussian(m,v)
    
    def __mul__(self,g):
        # Gaussian x Gaussian
        # mu = (var1*mu2 + var2*mu1)/(var1+var2)
        # var = (var1*var2)/(var1+var2)
        var2 = g.var()
        var1 = self.var() + 0.00000000001 # to avoid devided by zero
        mu1 = self.mean()
        mu2 = g.mean()
        mu = (var1*mu2 + var2*mu1)/(var1+var2)
        var = (var1*var2)/(var1+var2)
        return Gaussian(mu,var)
    
    def var(self):
        return self._var
    
    def std(self):
        return np.sqrt(self.var())
    
    def mean(self):
        return self._mean
    
    def size(self):
        return self._size
    
    
def combine(g1,g2):
    # to mix 2 samples together to get new one
    new_mean = (g1.mean()*g1.size() + g2.mean()*g2.size())/(g1.size()+g2.size()) #---(1)
    t1 = g1.size()*(g1.var()+math.pow(g1.mean(),2)- math.pow(new_mean,2)) # --- (2)
    t2 = g2.size()*(g2.var()+math.pow(g2.mean(),2)- math.pow(new_mean,2)) # --- (3)
    new_var = (t1+t2)/(g1.size()+g2.size())
    new_size=g1.size()+g2.size()
    
    return Gaussian(new_mean,new_var,new_size)
    
