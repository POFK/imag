#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
#vis=np.load('vis_0.000000_0.610865_128.npy')
#vis=np.load('vis_0.000000_0.610865_128_small.npy')
vis=np.load('vis_0.000000_0.610865_64_small.npy')
UVW=vis[:,:3].real
XYZ=vis[:,3:6].real
V  =vis[:,-1]

plt.figure('UV')
plt.scatter(UVW[:,0],UVW[:,1],s=20,c=np.log10(np.abs(V)))
#plt.scatter(-UVW[:,0],-UVW[:,1],s=20,c=np.log10(np.abs(V)))
#plt.scatter(UVW[:,0],UVW[:,1],s=30,c=V.real)
plt.colorbar()

#plt.figure('VW')
#plt.scatter(UVW[:,1],UVW[:,2],s=20,c=np.log10(np.abs(V)))
##plt.scatter(-UVW[:,1],-UVW[:,2],s=20,c=np.log10(np.abs(V)))
##plt.scatter(UVW[:,1],UVW[:,2],s=30,c=V.real)
#plt.colorbar()

#plt.figure('UW')
#plt.scatter(UVW[:,0],UVW[:,2],s=20,c=np.log10(np.abs(V)))
##plt.scatter(-UVW[:,0],-UVW[:,2],s=20,c=np.log10(np.abs(V)))
##plt.scatter(UVW[:,0],UVW[:,2],s=30,c=V.real)
#plt.colorbar()


plt.show()


