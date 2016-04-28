#!/usr/bin/env python
# coding=utf-8
import aipy
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from vis import Vis
from mpi4py import MPI
import sys
'''
usage:
    time mpirun -hostfile node_fast python get_vis.py BL_num split
    time mpirun -hostfile node_fast python get_vis.py 128 64
'''

##############################mpi util####################################
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

vis_root=None
UV_root=None
##############################init########################################
BL_num=int(sys.argv[1])
split=int(sys.argv[2])
#path_map = './gsm_80_H1024.npy'
path_map = './gsm_80_H2048.npy'
#path_map = './gsm_80.npy'
map=np.load(path_map)
map_nside=hp.get_nside(map)
freq = 80. * 10**6  # Mpc
D = 5.
BL_length = 800
#BL_length = 15
lam = 3. * 10**8 / freq
source = [0. / 180. * np.pi, 35. / 180. * np.pi]
Vis.__init__(source=source)
#==========
#split=32
#BL_num=256
#BL_num=128
#BL_num = 64
#==========
BL_ra = np.linspace(-0./6, 2*np.pi , 1*BL_num, endpoint=False)
BL_dec = np.linspace(-np.pi / 2, np.pi / 2, BL_num)

Vis.BaseLine(BL_ra, BL_dec)
BL_bl = BL_length * Vis.BL_xyz
BL_NUM=len(BL_bl)

#==========
#filename='_BL%d_0.5_allsky'%BL_NUM
#filename='_BL%d_%d_allsky_H1024'%(BL_length,BL_NUM)
#filename='_BL%d_%d_allsky_N256'%(BL_length,BL_NUM)
filename='_BL%d_%d_allsky_Nside2048'%(BL_length,BL_NUM)
#==========
if rank==0:
    print '='*40
    print 'Input map:',path_map[2:]
    print 'source:',source
    print 'freq  :',freq
    print 'D     :',D
    print 'BL_num:',BL_num**2
    print 'split :',split
    vis_root=np.empty([BL_NUM/split,4],dtype=np.complex128)
    UV_root=np.empty([BL_NUM,3],dtype=np.float)
#==========
###############calculating UVW####################
UV_bl=Vis.BL_radec
mpi_UV_bl_index=np.array_split(np.arange(len(UV_bl)),size)
UV = []
for i in mpi_UV_bl_index[rank]:
    UV.append(Vis.Get_UV_radec(source[0], source[1], bl=Vis.BL_radec[i])[0])
UV = np.array(UV,dtype=np.float)

##############################mpi util##########################################
theta, phi = hp.pix2ang(map_nside, np.arange(map_nside**2 * 12))
thphi=np.c_[theta,phi]
sigma=hp.ang2vec(theta,phi)

BL_bl_split=np.array_split(BL_bl,split)
for i in np.arange(len(BL_bl_split)):
    mpi_bl=np.array_split(BL_bl_split[i],size)
    vis=np.dot(np.exp(-2*np.pi/lam*1j*np.dot(mpi_bl[rank],sigma.T)),map)
    vis_result=np.c_[mpi_bl[rank],vis/(map_nside**2*12.)]
    comm.Gather(vis_result,vis_root,root=0)
    if rank==0:
#       print mpi_bl[rank]
#       print i,mpi_bl[rank]
#       print vis_result.shape
        print '%d...'%(i+1)
        if i==0:
            vis_all_root=np.vstack(vis_root)
        else:
            vis_all_root=np.vstack((vis_all_root,vis_root))

comm.Gather(UV,UV_root,root=0)
if rank==0:
    print UV_root.shape
    print vis_all_root.shape
    output=np.c_[UV_root,vis_all_root]
    print 'vis (U,V,W,X,Y,Z,vis):',output
    print 'vis.shape',output.shape
#   np.save('vis_%f_%f_%d'%(source[0],source[1],BL_num),output)
#   np.save('vis_sky_%f_%f_%d'%(source[0],source[1],BL_num),output)
    np.save('./Vis/vis'+filename+'.npy',output)
###############################to test data#####################################
if rank==0:
    test_data=np.c_[UV_root,BL_bl]
    f=open('./Vis/check'+filename+'.meta','w')
    f.writelines('Input map: %s   \n'%path_map[2:])
    f.writelines('source   : %f,%f\n'%(source[0],source[1]))
    f.writelines('freq     : %f   \n'%freq)
    f.writelines('D        : %f   \n'%D)
    f.writelines('BL_num   : %d   \n'%BL_num**2)
    f.writelines('BL_length: %d   \n'%BL_length)
    f.writelines('split_num: %d   \n'%split)
    f.writelines('Output   : ./Vis/vis%s.npy \n'%filename)
    f.close()
    print '='*40

