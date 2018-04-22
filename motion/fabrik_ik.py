import math

class FABRIK():
	def __init__(self,joints=None):
		self.joints = joints
		self.target = None
		self.links = []
		self.update_link()
		self.terolance = 0.1
	
	def update_link(self):
		if self.joints is None : return
		for i in range(len(self.joints)-1):
			self.links.append(self._distance(self.joints[i+1], self.joints[i]))
		
	def _distance(self,p1,p2):
		d = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
		return math.sqrt(d)	
		
	def _multiply_c2p(self,const,point):	
		return (const * point[0],const * point[1])
		
	def _sum_2p(self,p1,p2):
		return(p1[0]+p2[0],p1[1]+p2[1])	
		
	def get_total_length(self):
		s = 0
		for l in self.links:
			s +=l
		return s
					
	def set_terolance(self,terolance):
		self.terolance = terolance	
	
	def _solve_unreachable(self,target):
		for i in range(len(self.joints)-1)  :
				ri = self._distance(target,self.joints[i])
				ld = self.links[i]/ri
				self.joints[i+1] = self._sum_2p(
								self._multiply_c2p(1-ld, self.joints[i]) , 
								self._multiply_c2p(ld,target))
		return 
		
	def 	_solve_reachable(self,target):
		# target is reachable , set b as the root position
		b = self.joints[0]
		n = len(self.joints)
		# Check whether the distance between the end effector pn 
		# and the target t is greater than a tolerance. (tol)
		dif_a = self._distance(target, self.joints[n-1])
		while dif_a > self.terolance :
			# stage 1 : forward reaching
			# set the end effector p as target t
			self.joints[n-1] = target
			for i in range(n-2,-1,-1):
				# find the distance ri between the new joint position pj[i+1] and joint pi
				ri = self._distance(self.joints[i+1], self.joints[i])
				ld = self.links[i]/ri
				# find new position of pi
				self.joints[i] = self._sum_2p(self._multiply_c2p(1-ld, self.joints[i+1]) , 
												self._multiply_c2p(ld, self.joints[i]))
		
			# stage 2 : backward reaching
			# set root pj0 to b
			self.joints[0] = b
			for i in range(0,n-1) :
				# find distance ri, between new position  pj[i] and pj[i+1]
				ri = self._distance(self.joints[i+1], self.joints[i])
				ld = self.links[i]/ri
				# find new position of pi
				self.joints[i+1]= self._sum_2p(self._multiply_c2p(1-ld, self.joints[i]) , 
													self._multiply_c2p(ld, self.joints[i+1]))
					
			dif_a = self._distance(target,self.joints[n-1])
		
		return		
		
	def solve(self,target=(0,0)):	
		if self.joints is None : return None
		if len(self.joints) < 2 : return None
		if len(self.links) < 1 : return None
		dist = self._distance(target, self.joints[0]) # assume pj[0] is a root
		if dist > self.get_total_length():
			print("target is unreachable, change position !")
			self._solve_unreachable(target)
		else :
			self._solve_reachable(target)
		return self.joints
		
def test():
	pj = FABRIK(joints=[(1,5),(1,10),(1,15),(1,20)])
	targets = [(10,10),(1,1),(2,2),(3,3),(4,4)]		
	for t in targets :	
		print(pj.solve(t))
		print(pj.links)
	
if __name__ == "__main__":
	test()	
		
