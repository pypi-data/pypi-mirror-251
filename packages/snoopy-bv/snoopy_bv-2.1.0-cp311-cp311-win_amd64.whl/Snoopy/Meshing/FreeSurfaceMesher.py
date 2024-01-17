import numpy as np
from Snoopy.Meshing.structuredGrid import createRectangularGrid
from Snoopy.Meshing import Mesh
from Snoopy.Meshing.vtkTools import creatDiskGrid, createFreeSurfaceMesh


class FreeSurface(object):
    """Dataclass holding a free surface paramters
    """

    def generateAroundPoint( self, x_center, y_center ) :
        raise(NotImplementedError)

    def generateAroundMesh( self, hull ) :
        raise(NotImplementedError)

    def generateAroundHstarMesh( self, mesh ) :
        raise(NotImplementedError)



class FreeSurfaceRect(FreeSurface):
    def __init__(self, x=500, y = 500, dx = 10, dy = 10):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy


class FreeSurfacesCirc(FreeSurface):
    def __init__(self, r=500, dx = 10,dy = 10):
        self.r = r
        self.dx = dx
        self.dy = dy



class FreeSurfaceRectPlain(FreeSurfaceRect):

    def generateAroundMesh( self, hull ) :
        """
        """
        x, y, _ = hull.integrate_cob()
        return self.generateAroundPoint( x, y )


    def generateAroundHstarMesh( self, mesh ) :
        """
        """
        hull = mesh.getUnderWaterHullMesh(0)
        return self.generateAroundMesh( hull )


    def generateAroundPoint( self, x_center, y_center ) :
        return createRectangularGrid( np.arange( x_center-0.5*self.x, x_center+0.5*self.x, self.dx),
                                      np.arange( y_center-0.5*self.y, y_center+0.5*self.y, self.dy), z=0  )


class FreeSurfaceCircPlain(FreeSurfacesCirc):
    def generateAroundMesh( self, hull ) :
        """
        """
        x, y, _ = hull.integrate_cob()
        return self.generateAroundPoint(  x, y )

    def generateAroundHstarMesh( self, mesh ) :
        """
        """
        hull = mesh.getUnderWaterHullMesh(0)
        return self.generateAroundMesh( hull )

    def generateAroundPoint( self, x_center, y_center ) :
        return Mesh.FromPolydata( creatDiskGrid( self.r, self.dx, self.dy ), polygonHandling="triangulate" )




class FreeSurfaceCircHole(FreeSurfacesCirc):
    def generateAroundMesh( self, hull ) :
        """
        """
        x, y, _ = hull.integrate_cob()
        return createFreeSurfaceMesh( hull, self.r , self.dx, self.dy, x_center = x, y_center = y )

    def generateAroundHstarMesh( self, mesh ) :
        """
        """
        hull = Mesh(mesh.getUnderWaterHullMesh(0))
        return self.generateAroundMesh( hull )

