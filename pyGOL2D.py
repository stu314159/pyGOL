#!/usr/bin/env python
"""
demo program for 2D Game of Life implementation

"""

from mpi4py import MPI
import numpy as np


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
import sys
sys.path.insert(1,'.') #<-- for some reason this seems to be required for loading local modules
from vtkHelper import saveVelocityAndPressureVTK_binary as writeVTK
import GOL_partition_helper as gp

print "rank %d of %d ready to go"%(rank,size)

Nx = 4;
Ny = 4;
numPart = size

# rank 0 process do the partitioning.
# save the result to a binary data file "partition.gol"
# all processes will read this file

partFileName = "partition.gol"

if rank==0:
    partVert = gp.makePartition(Nx,Ny,numPart);
    print "partVert = ",partVert #<--- printed as a Python list
    np.array(partVert).astype('int32').tofile(partFileName) #saved as a numpy array

comm.Barrier() #everyone waits until rank 0 is done

# everyone reads the file
partVert = np.fromfile(partFileName,dtype='int32') #<-- loaded as a numpy array
# now all processes have partition information

myPart,intOffset = gp.getPartitionAndOffset(partVert,rank);
if rank==1:
   print "rank 1, myPart = ", myPart
   print "rank 1, intOffset = %d"%intOffset

# write to disk a partition map giving the global point number in order for all partitions

filename = 'partMap.b_dat'
amode = MPI.MODE_WRONLY | MPI.MODE_CREATE #<- bit mask for file mode
fh = MPI.File.Open(comm,filename,amode)
offset = intOffset*np.dtype(np.int32).itemsize
fh.Write_at_all(offset,myPart)
fh.Close()

comm.Barrier() # make sure everyone is done
# rank 0 load this file and print to screen
if rank==0:
    partMap = np.fromfile(filename,dtype='int32')
    print "rank 0, partition map: ", partMap
