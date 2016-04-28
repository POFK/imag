#!/usr/bin/env python
# coding=utf-8
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt

map1=np.load('../sky_2.npy')
map2=np.load('../sky_3.npy')
map3=np.load('../gsm_80.npy')
a=np.load('vis_BL1024_allsky_test32.npy')
b=np.load('vis_BL1024_allsky_test64.npy')
c=np.load('vis_BL1024_allsky_test512.npy')
va=a[:,-1]
vb=b[:,-1]
vc=c[:,-1]

#print map1.sum() /hp.get_nside(map1)
#print map2.sum() /hp.get_nside(map2)
#print map3.sum() /hp.get_nside(map3)

#print np.abs(va)
#print np.abs(vb)
#print np.abs(vc)
#plt.plot(np.abs(va),label='va')
#plt.plot(np.abs(vb),label='vb')
#plt.plot(np.abs(vc),label='vc')
#plt.show()

print a[:32].real[:,3:6]
#print (va/vb).real
#print (vb/vc).real
#print (va/vc).real
#plt.plot(np.abs(va/vb),label='a/b')
#plt.plot(np.abs(vb/vc),label='b/c')
#plt.plot(np.abs(va/vc),label='a/c')
#plt.legend()
#plt.show()
