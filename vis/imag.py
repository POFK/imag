#!/usr/bin/env python
# coding=utf-8
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from scipy import linalg
import sys
################################################################################
freq = 80. * 10**6  # Mpc
D = 5.
lam = 3. * 10**8 / freq
source = [0. / 180. * np.pi, 35. / 180. * np.pi]
#=======

################################################################################
file_name=sys.argv[1]
nside=int(sys.argv[2])
#file_name='./Vis/vis_BL4096_allsky.npy'
vis=np.load(file_name)
UVW=vis[:,:3].real
XYZ=vis[:,3:6].real
V=vis[:,-1]
#nside=64
theta, phi = hp.pix2ang(nside, np.arange(nside**2 * 12))
thphi=np.c_[theta,phi]
sigma=hp.ang2vec(theta,phi)
output='pix%d'%(nside)+file_name[9:-4] 

print '='*40
print 'Input :',file_name
print 'Output:',output

Beam_S=[]
for i in XYZ:
    Beam=np.exp(-2*np.pi/lam*1j*(sigma[:,0]*i[0]+sigma[:,1]*i[1]+sigma[:,2]*i[2])) #beam with i
    Beam_S.append(Beam)
Beam_S=np.array(Beam_S,dtype=np.complex128)  #shape is (time,direction)

shape=Beam_S.shape
################################################################################
#np.save('svd_U',svd_U)
#np.save('svd_s',svd_V)
#np.save('svd_V',svd_W)
#################   SVD  ######################################################
print 'pinv...'
print 'beam shape',Beam_S.shape
T_B=linalg.pinv2(a=Beam_S,cond=10**-6)
I_hat=np.dot(T_B,V)
#svd_U,svd_V,svd_W=np.linalg.svd(Beam_S)
##svd_V[svd_V<10**-6]=np.float('inf')
#S= np.zeros(shape, dtype=np.complex128)
#S[:len(svd_V),:len(svd_V)]=np.diag(1./svd_V)
#B0=np.dot(np.dot(svd_W.T,S.T),svd_U.T)
#print B0.shape
#print V.shape
#I=np.dot(B0,V)
#print I.shape
print 'pinv ok'
################################################################################
np.save('./recon_I/I_'+output+'.npy',I_hat)
I=np.abs(I_hat)
mean=I.mean()
std=I.std()
hp.mollview(I,title='recon_'+output,min=mean-1*std,max=mean+1*std)
plt.savefig('./png/recon_'+output+'.png')
#plt.show()
