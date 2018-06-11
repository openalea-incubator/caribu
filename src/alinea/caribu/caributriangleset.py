from alinea.caribu.display import generate_scene


class AbstractCaribuTriangleSet:
    def __init__(self):
        pass

    def getBoundingBox(self):
        pass

    def triangle_areas(self):
        pass

    def getZmin(self):
        pass

    def __getitem__(self, shapeid):
        """ Return all triangles of a shape """
        pass

    def keys(self):
        pass

    def values(self):
        pass

    def allvalues(self, copied=False):
        pass

    def allids(self):
        pass

    def items(self):
        pass

    def getNumberOfTriangles(self, shapeid):
        pass

    def generate_scene(self, colorproperty):
        pass



def CaribuTriangleSet(AbstractCaribuTriangleSet):
    def __init__(self, pointtuplelistdict):
        self.values = pointtuplelistdict
        self.allpoints = reduce(lambda x, y: x + y, self.values.values())

    def getBoundingBox(self):
        x, y, z = map(numpy.array, zip(*map(lambda x: zip(*x), self.allpoints)))
        return (x.min(), y.min(), z.min()), (x.max(), y.max(), z.max())        
        
    def triangle_areas(self):
        """ compute mean area of elementary triangles in the scene """

        def _surf(triangle):
            a, b, c = map(numpy.array, triangle)
            x, y, z = numpy.cross(b - a, c - a).tolist()
            return numpy.sqrt(x ** 2 + y ** 2 + z ** 2) / 2.0

        return numpy.array(map(_surf, self.allpoints))

    def getZmin(self):
        z = (pt[2] for tri in self.allpoints for pt in tri)
        return min(z)

    def getZmax(self):
        z = (pt[2] for tri in self.allpoints for pt in tri)
        return max(z)

    def __getitem__(self, shapeid):
        """ Return all triangles of a shape """
        return self.values[shapeid]

    def keys(self):
        return self.values.keys()

    def values(self):
        return self.values.values()

    def allvalues(self, copied=False):
        from copy import copy
        if copied : 
            return copy(self.allpoints)
        else:
            return self.allpoints

    def allids(self):
        groups = [[pid] * self.scene.getNumberOfTriangles(pid) for pid in self.scene.keys()]
        return reduce(lambda x, y: x + y, groups)

    def items(self):
        return self.values.items()

    def getNumberOfTriangles(self, shapeid):
        return len(self.values[shapeid])

    def generate_scene(self, colorproperty):
        return generate_scene(self.values, colorproperty)

