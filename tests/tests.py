from vector import vector

import math
import unittest

class TestGeom(unittest.TestCase):
    
    def test_vector(self):
        try:
            v=vector.Vector(*"abc")
        except TypeError:
            pass
        
        v=vector.Vector(1,1,0)
    
    def test_equal_tuple(self):
        v=vector.Vector(1,0,1)
        assert v == [1,0,1]
        
    def test_equal_list(self):
        v=vector.Vector(1,0,1)
        assert v == (1,0,1)
    
    def test_dot(self):
        v=vector.Vector(1,0,1)
        v2=vector.Vector(0,1,0)
        r=v.dot(v2)
        assert r==0
        
        v=vector.Vector(1,0,0)
        v2=vector.Vector(1,0,0)
        r=v.dot(v2)
        assert r==1
        
        v=vector.Vector(1,1,0)
        v2=vector.Vector(1,1,0)
        r=v.dot(v2)
        assert r==2
        
        v=vector.Vector(0,1,0)
        v2=vector.Vector(0,1,0)
        r=v.dot(v2)
        assert r==1
        
        v=vector.Vector(0,-1,0)
        v2=vector.Vector(0,-1,0)
        r=v.dot(v2)
        assert r==1
        
        v = vector.Vector(1,1,0)
        v = v.normalize()
        v2 = vector.Vector(1,1,0)
        v2 = v2.normalize()
        r = round(v.dot(v2),3)
        
        assert r==1
        
        v = vector.Vector(-1,-2,0)
        v = v.normalize()
        v2 = vector.Vector(-1,-2,0)
        v2 = v2.normalize()
        r = round(v.dot(v2),3)
        
        assert r == 1
    
    def test_normals_are_normalized(self):
        
        l = [(0,0,1),(1,0,1),(1,3,1),(0,3,1)]
        l = [vector.Vector(*x) for x in l]
        
        norms = vector.get_edge_normals(l)
        
        for x in norms:
            assert x.magnitude() == 1
    
    def test_get_edge_normals(self):
        
        l = [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
        l = [vector.Vector(*x) for x in l]
        
        norms = vector.get_edge_normals(l)
        
        comp = [(0.0, -1.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (-1.0, 0.0, 0.0),]
        
        c = 0
        m = len(l)
        while c < m:
            n = norms[c]
            compn= comp[c]
            assert n == compn
            c += 1
    def test_get_edge_normals_rot(self):
        
        axis = vector.Vector(1,0,0)
        axis = axis.normalize()
        angle = math.pi/2
        RM = vector.RotationMatrix(angle,axis)
        
        l = [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
        l = [RM * vector.Vector(*x) for x in l]
        
        norms = vector.get_edge_normals(l)
        
        comp = [(0.0, 0.0, -1.0),
        (1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0),
        (-1.0, 0.0, 0.0),
            ]
        
        
        c = 0
        m = len(l)
        while c < m:
            n = norms[c]
            compn = comp[c]
            assert n == compn
            c += 1
       
        
        

    
    def test_faked_3d_point_inside(self):
        l = [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
        l = [vector.Vector(*x) for x in l]
        vertlist = l
        point = vector.Vector(0.5,0.5,0.5)
        r = vector.get_faked_3d_point_inside(vertlist,point)
        assert r
        
        point = vector.Vector(0.5,0.4,0)
        r = vector.get_faked_3d_point_inside(vertlist,point)
        assert r
        
        point = vector.Vector(0.4,0.5,-0.5)
        r = vector.get_faked_3d_point_inside(vertlist,point)
        assert r
        
        point = vector.Vector(1,0.5,0.5)
        r = vector.get_faked_3d_point_inside(vertlist,point)
        assert not r
        
        point = vector.Vector(1.5,0.5,0.5)
        r = vector.get_faked_3d_point_inside(vertlist,point)
        assert not r
    
    def test_get_radians(self):
        
        c = 0
        m = 20
        while c < m:
            value1 = round(math.pi*2*(c/m),4)
            v1 = vector.Vector(math.cos(value1),math.sin(value1),0)
            value2 = round(v1.get_absolute_radians(),4)
            v2 = vector.Vector(math.cos(value2),math.sin(value2),0)
            assert round(v1.x,3) == round(v2.x,3)
            c += 1
        
    def test_position_input(self):
        # >>> from vector import vector
        # >>> l=[1,2]
        # >>> vector.Vector(*l,0)
        # (1, 2, 0)
        # >>> v=vector.Vector(*l,0)
        # >>> vector.Vector(*v,0)
        # Traceback (most recent call last):
          # File "<stdin>", line 1, in <module>
        # TypeError: Vector.__init__() takes 4 positional arguments but 5 were given
        # >>> 
        raise ValueError

    def test_angle_to_other(self):
        
        v1 = vector.Vector(1, 0, 0)
        v2 = vector.Vector(0, 1, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == math.pi/2
        
        v1 = vector.Vector(-1, 0, 0)
        v2 = vector.Vector(0, 1, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == math.pi/2
        
        v1 = vector.Vector(-1, 0, 0)
        v2 = vector.Vector(0, -1, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == math.pi/2
        
        v1 = vector.Vector(1, 0, 0)
        v2 = vector.Vector(0, -1, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == math.pi/2
        
        v1 = vector.Vector(-1, 1, 0)
        v2 = vector.Vector(1, 1, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == math.pi/2
        
        v1 = vector.Vector(-1, -1, 0)
        v2 = vector.Vector(1, -1, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == math.pi/2
        
        v1 = vector.Vector(1, 1, 0)
        v2 = vector.Vector(1, -1, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == math.pi/2
        
        v1 = vector.Vector(1, -1, 0)
        v2 = vector.Vector(1, 1, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == math.pi/2
        
        v1 = vector.Vector(1, 0, 0)
        v2 = vector.Vector(-1, 1, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == math.pi * 3/4
        
        v1 = vector.Vector(1, 0, 0)
        v2 = vector.Vector(-1, -1, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == math.pi * 3/4
        
        
        v1 = vector.Vector(1, 0, 0)
        v2 = vector.Vector(1, 0, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == 0
        
        # no idea
        v1 = vector.Vector(1, 0, 0)
        v2 = vector.Vector(0, 0, 0)
        try:
            rads_diff = v1.angle_to_other(v2)
        except ValueError:
            a=1
        
        v1 = vector.Vector(0, 0, 0)
        v2 = vector.Vector(1, 0, 0)
        try:
            rads_diff = v1.angle_to_other(v2)
        except ValueError:
            a=1
        
        v1 = vector.Vector(0, 0, 0)
        v2 = vector.Vector(0, 0, 0)
        try:
            rads_diff = v1.angle_to_other(v2)
        except ValueError:
            a=1
        
        v1 = vector.Vector(5, 0, 0)
        v2 = vector.Vector(5, 0, 0)
        rads_diff = v1.angle_to_other(v2)
        assert rads_diff == 0
        
        # this caused a math domain error in practice
        # because of floating points. so, let's keep the data around
        # for testing, this should just work, otherwise there is
        # a math error.
        v1 = vector.Vector(-2.512296313, 55.274074381, 0) 
        v2 = vector.Vector(-0.2512296313, 5.5274074381, 0)
        
        rads_diff = v1.angle_to_other(v2)
        
    def test_vector_interpolate(self):
        
        v1 = vector.Vector(1, 0, 0)
        v2 = vector.Vector(0, 1, 0)
        stepsize = 0.1
        vectors1 = []
        while True:
            v1_values = vector.vector_interpolation_step(v1, v2, stepsize)
            v1 = v1_values[0]
            v1 = vector.Vector(*v1)
            vectors1.append(v1)
            rads_diff = v1.angle_to_other(v2)
            if abs(rads_diff) < stepsize:
                break

        comp_values = [(0.995004, 0.099833, 0.0), (0.98006653406728, 0.198668509599154, 0.0), (0.955336645189015, 0.295519004911694, 0.0), (0.921061424274725, 0.389416795500676, 0.0), (0.8775833352777, 0.479423693144037, 0.0), (0.825336793435605, 0.56464038582662, 0.0), (0.764843824771546, 0.644215423297078, 0.0), (0.696708850224101,
                                                                                                                                                                                                                                                                                                                             0.71735372440966, 0.0), (0.621612646521137, 0.783324521249008, 0.0), (0.540305544137883, 0.841468660663524, 0.0), (0.45359993030249, 0.891205190253387, 0.0), (0.362362131955952, 0.932037163008717, 0.0), (0.267503759768537, 0.963556602600333, 0.0), (0.169972599699767, 0.985448579711952, 0.0), (0.070743143109733, 0.997494358684778, 0.0)]
        c = 0

        while c < len(comp_values):
            v1 = vectors1[c]
            v2 = vector.Vector(*comp_values[c])
            assert v1 == v2
            c += 1

        a = 1

        v1 = vector.Vector(0, 1, 0)
        v2 = vector.Vector(1, 0, 0)
        vectors2 = []
        while True:
            v1_values = vector.vector_interpolation_step(v1, v2, stepsize)
            v1 = v1_values[0]
            v1 = vector.Vector(*v1)
            vectors2.append(v1)
            rads_diff = v1.angle_to_other(v2)
            if abs(rads_diff) < stepsize:
                break

        comp_values = [(0.099833, 0.995004, 0.0), (0.198668509599154, 0.98006653406728, 0.0), (0.295519004911694, 0.955336645189015, 0.0), (0.389416795500676, 0.921061424274725, 0.0), (0.479423693144037, 0.8775833352777, 0.0), (0.56464038582662, 0.825336793435605, 0.0), (0.644215423297078, 0.764843824771546, 0.0), (0.71735372440966,
                                                                                                                                                                                                                                                                                                                             0.696708850224101, 0.0), (0.783324521249008, 0.621612646521137, 0.0), (0.841468660663524, 0.540305544137883, 0.0), (0.891205190253387, 0.45359993030249, 0.0), (0.932037163008717, 0.362362131955952, 0.0), (0.963556602600333, 0.267503759768537, 0.0), (0.985448579711952, 0.169972599699767, 0.0), (0.997494358684778, 0.070743143109733, 0.0)]
        c = 0

        while c < len(comp_values):
            v1 = vectors2[c]
            v2 = vector.Vector(*comp_values[c])
            assert v1 == v2
            c += 1

        v1 = vector.Vector(1, 1, 0)
        v1 = v1.normalize()
        v2 = vector.Vector(1, -1, 0)
        v2 = v2.normalize()
        vectors3 = []
        while True:
            v1_values = vector.vector_interpolation_step(v1, v2, stepsize)
            v1 = v1_values[0]
            vectors3.append(v1)
            rads_diff = v1.angle_to_other(v2)
            if abs(rads_diff) < stepsize:
                break

        comp_values = [(0.774166666993936, 0.632981484421543, 0.0), (0.833491542598757, 0.552531841907184, 0.0), (0.884488512471719, 0.4665615277866, 0.0), (0.926648035800461, 0.375929522187535, 0.0), (0.959548871914816, 0.281541382947523, 0.0), (0.982862289150868, 0.184340197651286, 0.0), (0.996355349402941, 0.08529716068629, 0.0), (0.999893235545641, -
                                                                                                                                                                                                                                                                                                                                                0.014598130533351, 0.0), (0.993440598471292, -0.114347563218466, 0.0), (0.977061910283725, -0.212954481938554, 0.0), (0.950920820119454, -0.30943364679418, 0.0), (0.915278519032604, -0.402821077530066, 0.0), (0.870491130280998, -0.492183685230536, 0.0), (0.817006151088586, -0.57662859536136, 0.0), (0.755357981436676, -0.655312069005989, 0.0)]

        while c < len(comp_values):
            v1 = vectors3[c]
            v2 = vector.Vector(*comp_values[c])
            assert v1 == v2
            c += 1

        v1 = vector.Vector(1, -1, 0)
        v1 = v1.normalize()
        v2 = vector.Vector(1, 1, 0)
        v2 = v2.normalize()
        vectors4 = []
        while True:
            v1_values = vector.vector_interpolation_step(v1, v2, stepsize)
            v1 = v1_values[0]
            rads_diff = v1.angle_to_other(v2)
            vectors4.append(v1)
            if abs(rads_diff) < stepsize:
                break

        while c < len(comp_values):
            v1 = vectors4[c]
            v2 = vector.Vector(*comp_values[c])
            assert v1 == v2
            c += 1

        if True:
            make_interpolation_picture(vectors1, 1)
            make_interpolation_picture(vectors2, 2)
            make_interpolation_picture(vectors3, 3)
            make_interpolation_picture(vectors4, 4)

        return

        
    def test_sub(self):
        v1=vector.Vector(-1.5,0,0)
        v2=vector.Vector(-0.5,0,0)
        assert v2-v1 == vector.Vector(1,0,0)
        
        
    def test_mirror_rotation(self):
        #I want the result to be at...
        #(0.9,0.9,0)
        #I expect the result to be at
        #(-0.1,-0.1,0)
        point=vector.Vector(0.3,0.1,0)
        
        axis=vector.Vector(1,-1,0)
        axis=axis.normalize()
        angle=3.14156
        assert axis == (0.7071067811865475, -0.7071067811865475, 0.0)
                
        M=vector.RotationMatrix(angle,axis)
        mid_point=vector.Vector(0.5,0.5,0)
        shifted_point=point-mid_point
        
        assert shifted_point == (-0.2, -0.4, 0)
        r=M*shifted_point
        
        r=round(r,2)
        assert r == (0.4, 0.2, -0.0)
        
        axis2=vector.Vector(0,0,1)
        angle2=3.14156/2
        M2=vector.RotationMatrix(angle2,axis2)
        r2=M2*point
        r2 = round(r2,3)
        assert r2 == (-0.1, 0.3, 0.0)

def make_interpolation_picture(vectors, filenameaddition):
    from geom import geom
    r = geom.rectangle(local_position=vector.Vector(-1.5, -1.5, 0), d_vec=vector.Vector(3, 3, 0))
    r.style = "fill:rgb(255,255,255);"
    l = [r]
    for v in vectors:
        l.append(geom.Line.from_two_points(vector.Vector(0, 0, 0), v))
        l[-1].style = f"stroke:rgb{(255*vectors.index(v)/len(vectors),0,0)};"
        
    fl = []
    for x in l:
        fl.append(x.as_svg())
    my_view_box_d = geom.make_view_box_d(l)
    fn = f"interptest{filenameaddition}.svg"
    geom.main_svg(fl,fn, view_box_d=my_view_box_d)


if __name__=="__main__":
    unittest.main()
