from vector import vector

import unittest

class TestGeom(unittest.TestCase):
    
    def test_vector(self):
        try:
            v=vector.Vector(*"abc")
        except TypeError:
            pass
        
        v=vector.Vector(1,1,0)
        
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
    
    def test_vector_interpolate(self):
        v1=vector.Vector(1,0,0)
        v2=vector.Vector(0,1,0)
        
        stepsize=0.5
        while True:
            v1=vector.vector_interpolation_step(v1,v2,stepsize)
            rads_diff=vector.angle_v1v2(v1,v2)
            if abs(rads_diff)<stepsize:
                break
        
        v1=vector.Vector(1,0,0)
        v2=vector.Vector(0,1,0)
        
        while True:
            v1=vector.vector_interpolation_step(v1,v2,stepsize)
            rads_diff=vector.angle_v1v2(v1,v2)
            if abs(rads_diff)<stepsize:
                break
        
        v1=vector.Vector(1,1,0)
        v1=v1.normalize()
        v2=vector.Vector(1,-1,0)
        v2=v2.normalize()
        while True:
            v1=vector.vector_interpolation_step(v1,v2,stepsize)
            rads_diff=vector.angle_v1v2(v1,v2)
            if abs(rads_diff)<stepsize:
                break
        
        v1=vector.Vector(1,1,0)
        v1=v1.normalize()
        v2=vector.Vector(1,-1,0)
        v2=v2.normalize()
        
        while True:
            v1=vector.vector_interpolation_step(v1,v2,stepsize)
            rads_diff=vector.angle_v1v2(v1,v2)
            
            if abs(rads_diff)<stepsize:
                break
        
if __name__=="__main__":
    unittest.main()
