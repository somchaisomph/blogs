'''
Erik Reinhard, Michael Ashikhmin, Bruce Gooch and Peter Shirley,
'Color Transfer between Images', IEEE CG&A special issue on Applied
Perception, Vol 21, No 5, pp 34-41, September - October 2001
'''
import matplotlib.pyplot as plt
import numpy as np
import skimage.io

def replaceZeroes(data):
        '''
        Reference :
        https://stackoverflow.com/questions/21610198/runtimewarning-divide-by-zero-encountered-in-log
        '''
        min_nonzero = np.min(data[np.nonzero(data)])
        data[data == 0] = min_nonzero
        return data

s_img_1 = skimage.io.imread('pexels-photo-248771.jpeg')
t_img_1 = skimage.io.imread('pexels-photo-440731.jpeg') 

ro = s_img_1.shape[0]
co = s_img_1.shape[1]

# normalize
s_img = s_img_1/255 
t_img = t_img_1/255

# split RBG channels
sR,sG,sB = np.rollaxis(s_img,-1)
tR,tG,tB = np.rollaxis(t_img,-1)

r1 = sR.reshape((sR.shape[0]*sR.shape[1],1))
g1 = sG.reshape((sG.shape[0]*sG.shape[1],1))
b1 = sB.reshape((sB.shape[0]*sB.shape[1],1))

r2 = tR.reshape((tR.shape[0]*tR.shape[1],1))
g2 = tG.reshape((tG.shape[0]*tG.shape[1],1))
b2 = tB.reshape((tB.shape[0]*tB.shape[1],1))

s_img = np.hstack((r1,g1,b1))
t_img = np.hstack((r2,g2,b2))

a = np.array([[0.3811, 0.5783, 0.0402],[0.1967, 0.7244, 0.0782],[0.0241, 0.1288 ,0.8444]])
b = np.array([[1/np.sqrt(3), 0 ,0],[0, 1/np.sqrt(6), 0],[0, 0, 1/np.sqrt(2)]])
c = np.array([[1, 1, 1],[1, 1, -2],[1, -1, 0]])
b2 = np.array([[np.sqrt(3)/3, 0, 0],[0, np.sqrt(6)/6, 0],[0, 0, np.sqrt(2)/2]])
c2 = np.array([[1, 1, 1],[1, 1, -1],[1, -2, 0]])

# to LMS space
s_lms = np.dot(a,s_img.T)
t_lms = np.dot(a,t_img.T)

# log 10
s_lms = replaceZeroes(s_lms)
s_log10_lms = np.where(s_lms > 0.0000000001, np.log10(s_lms), -10)

t_lms = replaceZeroes(t_lms)
t_log10_lms = np.where(t_lms > 0.0000000001, np.log10(t_lms), -10)

# to LAB space
p1 = np.dot(b , c)
s_lab =  np.dot(p1, s_log10_lms)
t_lab =  np.dot(p1, t_log10_lms)

# to statistics
s_mean = np.mean(s_lab,axis=1)
s_std  = np.std(s_lab,axis=1)

t_mean = np.mean(t_lab,axis=1)
t_std  = np.std(t_lab,axis=1)

sf = t_std/s_std

#apply the statistical alignment
res_lab = np.zeros(s_lab.shape)

for ch in range(0,3):
    res_lab[ch,:] = (s_lab[ch,:] - s_mean[ch])*sf[ch] + t_mean[ch]

# convert back to LMS
LMS_res=np.dot(np.dot(c2,b2),res_lab)

for ch in range(0,3) :
    LMS_res[ch,:] = np.power(10,LMS_res[ch,:])

# convert back to RGB
d = np.array([[4.4679, -3.5873, 0.1193],[-1.2186, 2.3809, -0.1624],[0.0497, -0.2439, 1.2045]])

est_im = np.dot(d,LMS_res).T
result = est_im.reshape((ro,co,3)); # reshape the image

fig=plt.figure(figsize=(30,10))
fig.add_subplot(1,3,1)
plt.imshow(s_img_1)
plt.title('Source')
plt.axis('off')

fig.add_subplot(1,3,2)
plt.imshow(t_img_1)
plt.title('Target')
plt.axis('off')

fig.add_subplot(1,3,3)
plt.imshow(result)
plt.title('Result')
plt.axis('off')

plt.show()
