
import math

class MiSGIK():#stands for Mini Simple Geometry Inverse Kinematics :-)
 def __init__(self,l1,l2,unit='degrees'):
  self.l1 = l1
  self.l2 = l2
  self.unit=unit

 def _distance(self,target=(1,1)):
  # compute h value
  return math.sqrt(target[0]**2+target[1]**2)
 
 def _law_of_cosine(self,a,b,c):
  cos = (a**2+b**2-c**2)/(2*a*b)
  #cos must be in range of [-1,1]
  if cos < -1 : cos = -1
  if cos > 1 : cos = 1
  ang = math.acos(cos)
  return ang
 
 def solve(self,target=(1,1)):
  # parameters : x,y = coordinate of target, l1= lower arm length, l2 = upper arm lenght
  #to find theta1, theta2 for any given (x,y) position in term of A1,A2
  # where A1  = D1 + D2 , the angle of lower arm and A2 = angle of  upper arm
  # find distance between origin and target x,y
  dist = self._distance(target)
  alpha = math.atan2(target[1],target[0]) # in radian
  beta = self._law_of_cosine(dist,self.l1,self.l2)
  theta1 = alpha + beta
  theta2 = self._law_of_cosine(self.l1,self.l2,dist)
  if self.unit == 'degrees':
   ang_a1 = math.degrees(theta1)
   ang_a2 = math.degrees(theta2)  
   return (int(round(ang_a1)),int(round(ang_a2))) 
  else :
   return (theta1,theta2) 

#--- End of class ---
 
def test():
   myik = MiSGIK(l1=10,l2=10,unit='degrees')
   x = [1,2,3,4,5,6,7,8,9,10]
   y = [1,2,3,4,5,6,7,8,9,10]
   for i in range(len(x)):
       a1,a2 = myik.solve((x[i],y[i]))
       print("Target at [{0},{1}], Angles are {2} {3}".format(x[i],y[i],a1,180-a2))
 
if __name__ == "__main__":
 test()

