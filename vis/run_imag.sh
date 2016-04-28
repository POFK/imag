#!/bin/bash
time mpirun -hostfile node_fast python get_vis.py 128 128
time mpirun -hostfile node_fast python get_vis.py 64 64
time mpirun -hostfile node_fast python get_vis.py 32 64
#time mpirun -hostfile node_fast python get_vis.py 128 64

#time python imag.py ./Vis/vis_BL1024_allsky.npy  64
#time python imag.py ./Vis/vis_BL4096_allsky.npy  64
#time python imag.py ./Vis/vis_BL16384_allsky.npy 32
#time python imag.py ./Vis/vis_BL65536_allsky.npy 32
