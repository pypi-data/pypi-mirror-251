'''Defines mesh'''

import numpy as np
from .readWriteFiles import readMesh

class mesh3D():
    '''Defines properties of a mesh'''

    def __init__(self, filePath, scale):
        self.mesh = readMesh(filePath)
        self.scale = float(scale)
        self.mesh = self.mesh.apply_scale(self.scale)

        # Mesh properties
        self.isWaterTight = self.mesh.is_watertight
        self.bounds = self.mesh.bounds
        self.meshOrigin = self.origin()

    def isInside(self, point):
        '''Check if point is inside the mesh'''
        adjustedPoint = [point[i] +self.meshOrigin[i] for i in range(3)]
        return self.mesh.contains([point])[0]
    
    def volume(self):
        return self.mesh.volume
    
    def surfaceArea(self):
        return self.mesh.area
    
    def origin(self):
        return [0, 0, 0]
    
    def findCenter(self):
        return self.origin