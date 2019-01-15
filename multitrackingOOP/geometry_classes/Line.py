import numpy as np


class Line:
    def __init__(self, x=0, y=0, z=0, dx=0, dy=0, dz=0, point=[], direction=[], params=[], silicon_id=0,
                 start=None, end=None):
        if len(params) == 6:
            self.x, self.y, self.z = params[:3]
            self.dx, self.dy, self.dz = params[3:]
        elif len(params) == 5:
            self.x, self.y = params[:2]
            self.z = z
            self.dx, self.dy, self.dz = params[2:]
        elif len(point) == 3 and len(direction) == 3:
            self.x, self.y, self.z = point
            self.dx, self.dy, self.dz = direction
        elif start is not None and end is not None:
            self.x, self.y, self.z = start.x, start.y, start.z
            self.dx, self.dy, self.dz = self.normalized_vector(start, end)
        else:
            self.x, self.y, self.z = x, y, z
            self.dx, self.dy, self.dz = dx, dy, dz

        self.x = float(self.x)
        self.y = float(self.y)
        self.z = float(self.z)
        self.dx = float(self.dx)
        self.dy = float(self.dy)
        self.dz = float(self.dz)

        # just to make this line a detector Line
        self.silicon_id = int(silicon_id)

    def __repr__(self):
        return "Line: det = {}\t p = ({:.6f}, {:.6f}, {:.6f})\t v = [{:.6f}, {:.6f}, {:.6f}]".format(
            self.silicon_id, self.x, self.y, self.z, self.dx, self.dy, self.dz)

    def distance(self, other):
        n_vector = cross_product(self.line_vector(), other.line_vector())
        s_o_vector = [self.x - other.x, self.y - other.y, self.z - other.z]
        distance = abs(dot_product(n_vector, s_o_vector)) / linalg_norm(n_vector)

        return distance

    def line_vector(self):
        return [self.dx, self.dy, self.dz]

    def line_vector_old(self):
        return np.array([self.dx, self.dy, self.dz])

    # TODO: Test that method
    def xy_on_z(self, z):
        delta_z = z - self.z
        k_z = delta_z / self.dz

        new_x = self.x + k_z * self.dx
        new_y = self.y + k_z * self.dy

        return new_x, new_y

    def y_on_x(self, x):
        return (x - self.x) / self.dx * self.dy + self.y

    def normalized_vector(self, start, end):
        vector_dx = end.x - start.x
        vector_dy = end.y - start.y
        vector_dz = end.z - start.z

        return self.normalize(vector_dx, vector_dy, vector_dz)

    def normalize(self, dx, dy, dz):
        v = [dx, dy, dz]
        v_norm = linalg_norm(v)

        return dx / v_norm, dy / v_norm, dz / v_norm

    '''
    TODO: check if this code works
    '''

    def normalize_line_vector(self):
        line_vector = [self.dx, self.dy, self.dz]
        line_vector_norm = linalg_norm(line_vector)

        self.dx = self.dx / line_vector_norm
        self.dy = self.dy / line_vector_norm
        self.dz = self.dz / line_vector_norm


def cross_product(v_a, v_b):
    a_x, a_y, a_z = v_a
    b_x, b_y, b_z = v_b

    return [a_y * b_z - a_z * b_y,
            a_z * b_x - a_x * b_z,
            a_x * b_y - a_y * b_x]


def linalg_norm(v_a):
    a_x, a_y, a_z = v_a
    return np.sqrt(a_x * a_x + a_y * a_y + a_z * a_z)


def dot_product(v_a, v_b):
    a_x, a_y, a_z = v_a
    b_x, b_y, b_z = v_b

    return a_x * b_x + a_y * b_y + a_z * b_z
