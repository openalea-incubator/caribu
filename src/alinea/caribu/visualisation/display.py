import openalea.plantgl.all as pgl


# TODO: store data (optics and transparencies in the scene
# Methods to color the scene, and the vertices.
# Add static methods to the scene
# test it with randomized values and color map
# Implement discrete color map (lut?)

class CanestraScene:
    def __init__(self, plants, soil, indexes):
        self.plants = plants
        self.soil = soil
        self.indexes = indexes
        self.scene = None

    def build_scene(self,
                    leaf_material=None,
                    stem_material=None,
                    soil_material=None):
        if not leaf_material:
            leaf_material = pgl.Material(pgl.Color3(0, 180, 0))

        if not stem_material:
            stem_material = pgl.Material(pgl.Color3(0, 130, 0))
        if not soil_material:
            soil_material = pgl.Material(pgl.Color3(170, 85, 0))

        scene = pgl.Scene()
        for id, plant in self.plants.items():
            leaves = plant["leaves"]
            stems = plant["stems"]
            for lid, leaf in leaves.items():
                shape = pgl.Shape(leaf, leaf_material)
                shape.name = str(lid)
                scene.add(shape)
            if len(stems.pointList) > 0:
                shape = pgl.Shape(stems, stem_material)
                shape.name = str(id)
                scene.add(shape)
        if "soil" in self.soil:
            shape = pgl.Shape(self.soil["soil"], soil_material)
            scene.add(shape)

        self.scene = scene

    def build_scene_with_colors(self, colors):
        scene = pgl.Scene()
        n = len(colors)
        for i, (label, count) in enumerate(self.indexes):
            pid = plant_id(label)
            plant = self.plants[pid]
            if is_leaf(label):
                lid = leaf_id(label)
                geom = plant["leaves"][lid]
            elif is_stem(label):
                geom = plant["stems"]
            else:
                geom = self.soil["soil"]
            if count == 0:
                geom.colorList = []
                geom.colorPerVertex = False

            assert 3 * len(geom.colorList) == count
            if i >= n or type(colors[i]) is float:
                geom.colorList.append(pgl.Color4(10, 10, 10, 0))
            else:
                r, g, b = colors[i]
                geom.colorList.append(pgl.Color4(r, g, b, 0))

        for plant in list(self.plants.values()):
            leaves = plant["leaves"]
            stems = plant["stems"]
            for leaf in list(leaves.values()):
                scene += leaf
            if len(stems.pointList) > 0:
                scene += stems
        if "soil" in self.soil:
            scene += self.soil["soil"]

        self.scene = scene

    def plot(self, colors=None):
        if not self.scene and not colors:
            self.build_scene()
        if colors:
            self.build_scene_with_colors(colors)

            pgl.Viewer.display(self.scene)


def process_line(line):
    line = line.strip()
    if not line:
        return
    if line[0] == '#':
        return

    l = line.split()
    nb_polygon = int(l[-10])
    assert nb_polygon == 3
    coords = list(map(float, l[-9:]))
    label = l[2]
    if len(label) < 11:
        label = (12 - len(label)) * '0' + label

    triangle = (pgl.Vector3(*coords[:3]),
                pgl.Vector3(*coords[3:6]),
                pgl.Vector3(*coords[6:]))
    return label, triangle


def read(fn):
    f = open(fn)
    elements = []
    for l in f.readlines():
        elt = process_line(l)
        if elt:
            elements.append(elt)
    f.close()
    return elements


def build_geometry(elements):
    plants = {}
    soil = {}
    indexes = []
    print('number of elements', len(elements))
    for i, (label, triangle) in enumerate(elements):
        pid = plant_id(label)
        if pid not in plants:
            plants[pid] = {"leaves": {}, "stems": pgl.TriangleSet([], [])}

        plant = plants[pid]

        if is_leaf(label):
            lid = leaf_id(label)
            leaves = plant['leaves']
            if lid not in leaves:
                leaves[lid] = pgl.TriangleSet([], [])
            shape = leaves[lid]
        elif is_stem(label):
            shape = plant['stems']
        else:
            assert is_soil(label)
            if "soil" not in soil:
                soil["soil"] = pgl.TriangleSet([], [])
            shape = soil["soil"]

        count = len(shape.pointList)
        shape.pointList.append(triangle[0])
        shape.pointList.append(triangle[1])
        shape.pointList.append(triangle[2])
        shape.indexList.append(pgl.Index3(count, count + 1, count + 2))
        indexes.append((label, count))

    return CanestraScene(plants, soil, indexes)


def optical_species(label):
    return int(label[:-11])


def plant_id(label):
    return int(label[-11:-6])


def transparency(label):
    return int(bool(leaf_id(label)))


def leaf_id(label):
    return int(label[-6:-3])


def is_soil(label):
    return optical_species(label) == 0 and transparency(label) == 0


def is_leaf(label):
    return leaf_id(label) > 0


def is_stem(label):
    return (not is_leaf(label)) and (not is_soil(label))


def transparencies(indexes):
    return [transparency(t[0]) for t in indexes]


def optics(indexes):
    return [optical_species(t[0]) for t in indexes]

# def test(fn):
#     elements = read(fn)
#     plants, soil, indexes = build_geometry(elements)
#     scene = build_scene(plants, soil)
#     pgl.Viewer.display(scene)
