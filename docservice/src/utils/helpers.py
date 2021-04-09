

class Helpers(object):
    @classmethod
    def vertices_to_boundingbox(self, vertices):
        c1, c2, c3, c4  = vertices[0], vertices[1], vertices[2], vertices[3]
        left, top       = c1['x'], c1['y']
        width, height   = (c3['x'] - c1['x']), (c3['y'] - c1['y'])
        return (left, top, width, height)