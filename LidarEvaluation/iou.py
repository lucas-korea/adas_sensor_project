
### calculate iou
# reference: https://stackoverflow.com/questions/44797713/calculate-the-area-of-intersection-of-two-rotated-rectangles-in-python
from math import pi, cos, sin

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        if not isinstance(v, Vector):
            return NotImplemented
        return Vector(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        if not isinstance(v, Vector):
            return NotImplemented
        return Vector(self.x - v.x, self.y - v.y)

    def cross(self, v):
        if not isinstance(v, Vector):
            return NotImplemented
        return self.x*v.y - self.y*v.x


class Line:
    # ax + by + c = 0
    def __init__(self, v1, v2):
        self.a = v2.y - v1.y
        self.b = v1.x - v2.x
        self.c = v2.cross(v1)

    def __call__(self, p):
        return self.a*p.x + self.b*p.y + self.c

    def intersection(self, other):
        # See e.g.     https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Using_homogeneous_coordinates
        if not isinstance(other, Line):
            return NotImplemented
        w = self.a*other.b - self.b*other.a
        return Vector(
            (self.b*other.c - self.c*other.b)/w,
            (self.c*other.a - self.a*other.c)/w
        )


def rectangle_vertices(cx, cy, w, h, r):
    # angle = pi*r/180
    angle = r
    dx = w/2
    dy = h/2
    dxcos = dx*cos(angle)
    dxsin = dx*sin(angle)
    dycos = dy*cos(angle)
    dysin = dy*sin(angle)
    return (
        Vector(cx, cy) + Vector(-dxcos - -dysin, -dxsin + -dycos),
        Vector(cx, cy) + Vector( dxcos - -dysin,  dxsin + -dycos),
        Vector(cx, cy) + Vector( dxcos -  dysin,  dxsin +  dycos),
        Vector(cx, cy) + Vector(-dxcos -  dysin, -dxsin +  dycos)
    )

def intersection_area_xy(r1, r2):
    # r1 and r2 are in (center, width, height, rotation) representation
    # First convert these into a sequence of vertices

    rect1 = rectangle_vertices(*r1)
    rect2 = rectangle_vertices(*r2)

    # Use the vertices of the first rectangle as
    # starting vertices of the intersection polygon.
    intersection = rect1

    # Loop over the edges of the second rectangle
    for p, q in zip(rect2, rect2[1:] + rect2[:1]):
        if len(intersection) <= 2:
            break # No intersection

        line = Line(p, q)

        # Any point p with line(p) <= 0 is on the "inside" (or on the boundary),
        # any point p with line(p) > 0 is on the "outside".

        # Loop over the edges of the intersection polygon,
        # and determine which part is inside and which is outside.
        new_intersection = []
        line_values = [line(t) for t in intersection]
        for s, t, s_value, t_value in zip(
            intersection, intersection[1:] + intersection[:1],
            line_values, line_values[1:] + line_values[:1]):
            if s_value <= 0:
                new_intersection.append(s)
            if s_value * t_value < 0:
                # Points are on opposite sides.
                # Add the intersection of the lines to new_intersection.
                intersection_point = line.intersection(Line(s, t))
                new_intersection.append(intersection_point)

        intersection = new_intersection

    # Calculate area
    if len(intersection) <= 2:
        return 0

    return 0.5 * sum(p.x*q.y - p.y*q.x for p, q in
                     zip(intersection, intersection[1:] + intersection[:1]))

def intersection_height_z(h1,h2):
    bottom_z1, size_z1 = h1
    bottom_z2, size_z2 = h2

    top_z1 = bottom_z1 + size_z1
    top_z2 = bottom_z2 + size_z2

    if bottom_z1 <= bottom_z2 and bottom_z2 <= top_z1:
        bottom = bottom_z2
    elif bottom_z2 <= bottom_z1 and bottom_z1 <= top_z2:
        bottom = bottom_z1
    else:
        return 0

    if bottom_z1 <= top_z2 and top_z2 <= top_z1:
        top = top_z2
    elif bottom_z2 <= top_z1 and top_z1 <= top_z2:
        top = top_z1
    else:
        return 0

    return top - bottom

def calculate_area(r1):
    _, _, w, h, _ = r1

    return w*h

def calculate_2d_IoU(area1, area2, intersection):
    den = intersection
    num = area1 + area2 - intersection
    if num != 0:
        return den/num

def calculate_3d_IoU(volume1, volume2, intersection):
    num = intersection
    den = volume1 + volume2 - intersection
    if den != 0:
        return num/den

def expand_bbox(bbox_data):
    return bbox_data[0], bbox_data[1], bbox_data[2], bbox_data[3],\
           bbox_data[4], bbox_data[5], bbox_data[6], bbox_data[7], bbox_data[8]

def evaluate_IoU(bbox_gt, bbox_output, IoU_Criterion):
    IoU = IoU_Criterion
    '''
    Calculate IOU of each frame
    '''
    
    # our label: id, center x, center y, bottom z, size x, size y, size z, yaw [rad], obj_cls -> it can be directly used in the function
    # bbox: center x, center y, bottom z, size x, size y, size z, yaw [deg]
    id_gt, x_gt, y_gt, z_gt, sx_gt, sy_gt, sz_gt, yaw_gt, obj_cls_gt = expand_bbox(bbox_gt)
    id_output, x_output, y_output, z_output, sx_output, sy_output, sz_output, yaw_output, obj_cls_output = expand_bbox(bbox_output)
    # rectangle: center x, center y, size x, size y, yaw [deg]
    rectangle_gt = (x_gt, y_gt, sx_gt, sy_gt, yaw_gt)
    rectangle_output = (x_output, y_output, sx_output, sy_output, yaw_output)

    # height: bottom z, size z
    height_gt = (z_gt, sz_gt)
    height_output = (z_output, sz_output)
    area_gt = calculate_area(rectangle_gt)
    area_output = calculate_area(rectangle_output)

    height_intersection = intersection_height_z(height_gt,height_output)
    area_intersection = intersection_area_xy(rectangle_gt, rectangle_output)

    IoU_2D = calculate_2d_IoU(area_gt, area_output, area_intersection)

    volume_gt = area_gt*sz_gt
    volume_output = area_output*sz_output
    volume_intersection = area_intersection * height_intersection
    
    IoU_3D = calculate_3d_IoU(volume_gt, volume_output, volume_intersection)
    '''
    Compare the result
    '''
    if IoU_3D > IoU:
        flag_detected = True
    else:
        flag_detected = False

    
    return IoU_3D, flag_detected

