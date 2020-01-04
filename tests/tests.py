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
    
    def test_vars(self):
        from goodmath import symbol,boiler,solvers
        
        x,y,z=symbol.symbols(["x","y","z"])
        v=vector.Vector(x,y,z)
        v2=vector.Vector(1,1,0)
        r=v.dot(v2)
        print(r)
        assert r == boiler.sympify("x*1+y*1+z*0")
        
if __name__=="__main__":
    unittest.main()
