#!/usr/bin/env python
# coding=utf-8
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from scipy import linalg

map=np.load('sky_2.npy')
shape=len(map)
#hp.mollview(np.log10(map))
#plt.show()
Beam=np.random.randn(64*64,shape)
vis=np.dot(Beam,map)
S=np.dot(Beam.T,Beam)
T_b=linalg.pinv2(Beam)
II=np.dot(T_b,vis)
print np.allclose(map,II)
map_m=map.mean()
map_s=map.std()
hp.mollview(map,min=map_m-map_s,max=map_m+map_s,title='map')
im_m=II.mean()
im_s=II.std()
hp.mollview(II,min=im_m-im_s,max=im_m+im_s)
plt.savefig('test64_64.png')
plt.show()

