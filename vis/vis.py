#!/usr/bin/env python
# coding=utf-8
import numpy as np
import healpy as hp
import aipy
class Vis(object):
    @classmethod
    def __init__(self,source):
        self.H=source[0]
        self.D=source[1]
    @classmethod
    def D_angle(self,a,b):
        '''a and b is vector with (x,y,z)
        usage:
        a=np.array([1,1,0])
        b=np.array([2,0,0])
        print Vis.D_angle(a,b)/np.pi'''
        cos=np.dot(a,b)/(np.sqrt(a[0]**2+a[1]**2+a[2]**2)*np.sqrt(b[0]**2+b[1]**2+b[2]**2))
        self.angle=np.arccos(cos)
        return self.angle
    @classmethod
    def BaseLine(self,ra,dec):
        '''ra and dec is numpy.array'''
        R,D=np.meshgrid(ra,dec)
        self.BL_radec=np.c_[R.reshape(-1),D.reshape(-1)]
        self.BL_xyz=np.array([aipy.coord.radec2eq(i) for i in self.BL_radec])
#       return self.BL_xyz
    @classmethod
    def convert_xyz2uv(self,H,delta):
        '''H,delta is the source direction
        with ra,dec
        '''
        H=-H
        self.convert_matrix=np.array([[np.sin(H),np.cos(H),0],
            [-np.sin(delta)*np.cos(H),np.sin(delta)*np.sin(H),np.cos(delta)],
            [np.cos(delta)*np.cos(H),-np.cos(delta)*np.sin(H),np.sin(delta)]])
        return self.convert_matrix
    @classmethod
    def Get_UV_xyz(self,bl,freq):
        '''bl: baseline in xyz'''
        bl=np.array(bl)
        self.ls=3.0*10**8  #light_speed
        u,v,w=freq/self.ls*np.dot(self.convert_matrix,bl)
        return [u,v,w]
    @classmethod
    def Get_UV_radec(self,ra_source,dec_source,bl,freq=80*10**6):
        '''bl: baseline in ra_dec'''
        H=ra_source
        D=dec_source
        ls=3.0*10**8
        h=bl[0]
        d=bl[1]
        l=np.cos(d)*np.sin(h-H)
        m=(np.sin(d)*np.cos(D)-np.cos(d)*np.sin(D)*np.cos(H-h))
        n=(np.sin(d)*np.sin(D)+np.cos(d)*np.cos(D)*np.cos(H-h))
        U=freq/ls*np.cos(d)*np.sin(h-H)
        V=freq/ls*(np.sin(d)*np.cos(D)-np.cos(d)*np.sin(D)*np.cos(H-h))
        W=freq/ls*(np.sin(d)*np.sin(D)+np.cos(d)*np.cos(D)*np.cos(H-h))
        self.UVW=[U,V,W]
        self.lmn=[l,m,n]
        return self.UVW,self.lmn 
    @classmethod
    def Get_lmn(self,los,bl,freq=80*10**6):
        '''bl: ra, dec of the direction
        los: line of sight,like [np.pi,0]'''
        H=los[0]
        D=los[1]
        h=bl[:,0]
        d=bl[:,1]
        l=np.cos(d)*np.sin(h-H)
        m=(np.sin(d)*np.cos(D)-np.cos(d)*np.sin(D)*np.cos(H-h))
        n=(np.sin(d)*np.sin(D)+np.cos(d)*np.cos(D)*np.cos(H-h))
        lmn=np.c_[l,m,n]
        return lmn 




