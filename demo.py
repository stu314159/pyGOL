from pymetis import part_graph #<-- need PrgEnv-intel for this to work (I think...)
from vtkHelper import saveStructuredPointsVTK_ascii


def set_adjacency(Nx,Ny,ex,ey):
    """
    Nx = num of board positions in X-direction
    Ny = num of board positions in Y-direction
    ex = x-component of direction to neighbors
    ey = y-component of direction to neighbors
    
    
    returns adjDict = dictionary where the keys are the global lattice point numbers
    and the values are lists of neighboring lattice points
    
    
    """
    adjDict = {}
    
    for y in range(Ny):
      for x in range(Nx):
        gid = x + y*Nx
        for spd in range(len(ex)):
           dx = int(ex[spd]); dy = int(ey[spd]); 
           tx = (x+dx)%Nx; ty= (y+dy)%Ny; # target x- and y- cell numbers
           tid = tx+ty*Nx; # target point global id
           adjDict.setdefault(gid,[]).append(tid)
                    
    return adjDict

boardSize = 10 # assume a boardSize x boardSize game board
ex = [1, 0, -1 ,0, 1, -1, -1, 1]
ey = [0, 1, 0, -1, 1, 1, -1, -1]
numParts = 3 # specify the number of partitions

adjDict = set_adjacency(boardSize,boardSize,ex,ey)

cuts,part_vert = part_graph(numParts,adjDict) # find documentation on this.
dims = [boardSize, boardSize,1]
origin = [0,0,0]
spacing = [1,1,1]
saveStructuredPointsVTK_ascii(part_vert,'partitions','partition_metis.vtk',dims,origin,spacing)

print "cuts = ", cuts
print "part_vert = " 
print part_vert

