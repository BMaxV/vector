
import math
"""
This module assumes you know your way around linear algebra and python.
It will _not: warn you that something you're doing might not be what
you want to do. It'll rather do it and fail gracefull.

"""


def curl():
    raise NotImplemented
    """
    Takes a vectorfield and the base symbols to be differentiated with.
    If no base is provided, sympy symbols x,y,z are assumed.
    """
    
def divergence():
    """returns the sum of the components of the gradient vector"""
    raise NotImplemented
        

def gradient():
    """assumes all free symbols in the expression to be relevant variables.
    e.g. 
    (1,1,1) for f(x,y,z)=x+y+z
    (yz,xz,xy) for f(x,y,z)=x*y*z
    """
    raise NotImplemented
    
class Matrix:
    """ 
    3x3 matrix, takes vectors as input    
    """
    def __init__(self,v1,v2,v3):
        self.v1=v1
        self.v2=v2
        self.v3=v3
        
    def __getitem__(self,ind):
        if ind==0:
            return self.v1
        elif ind==1:
            return self.v2
        elif ind==2:
            return self.v3
        else:
            raise ValueError
    
    def __repr__(self):
        s="\n"
        c1=0
        c2=0
        m=3
        while c1 < m:
            while c2 < m:
                s+=str(self[c1][c2])+" "
                c2+=1
            s+="\n"
            c2=0
            c1+=1
        return s
    
    def __mul__(self,other):
        if isinstance(other,Matrix):
            new_vs=[]
            for v in other:
                rv=self*v
                new_vs.append(rv)
            M=Matrix(*new_vs)
            return M
        if isinstance(other,Vector):
            i=0
            j=0
            new_values=[]
            while i < 3:
                s=0
                while j < 3:
                    
                    val1=self[j][i]
                    val2=other[j]
                    r=val1*val2
                    s+=r
                    j+=1
                
                new_values.append(s)
                
                j=0
                i+=1
                
            V=Vector(*new_values)
            V=round(V,15)
            return V


    def from_Rotation(self,target,z):
        """ takes two vectors, rotation axis is calculated as cross product
        then rotation is applied as acos of the dot product"""
        
        rot_axis=target.cross(z)
        angle=math.acos(target.dot(z))
        M=self.Rotation(angle,None,rot_axis)
        
        return M
        
def RotationsMatrixFromVector(rot_vector):
    """not entirely confident this is correct"""
    
    rotations=[]
    if rot_vector[0]!=0:
        xrot=RotationMatrix(rot_vector[0],(1,0,0))
        rotations.append(xrot)
        
    if rot_vector[1]!=0:
        yrot=RotationMatrix(rot_vector[1],(0,1,0))
        rotations.append(yrot)
        
    if rot_vector[2]!=0:
        zrot=RotationMatrix(rot_vector[2],(0,0,1))
        rotations.append(zrot)
        
    return rotations

def RotationMatrix(angle,rot_axis):
    """angle in radians"""
    c=math.cos(angle)
    s=math.sin(angle)
    
    x=rot_axis[0]
    y=rot_axis[1]
    z=rot_axis[2]
    
    t=1-c
    v1=Vector(t*x**2+c  ,t*x*y+z*s,t*x*z-y*s)
    v2=Vector(t*x*y-z*s ,t*y**2+c,t*y*x+x*s)
    v3=Vector(t*x*z+y*s ,t*y*z-x*s,t*z**2+c)
    M=Matrix(v1,v2,v3)
    return M

class Vector:
    
    def __init__(self,x,y,z):
        """
        Works basically like a list or a tuple, except it supports
        common vector funtions.
        """
        
        #duck type check
        1+x,1+y,1+z
        
        self.x = x 
        self.y = y 
        self.z = z 
    
    
    def __lt__(self,other):
        if type(other)!=Vector:
            raise TypeError
        return self.magnitude()<other.magnitude()
        
    def __gt__(self,other):
        if type(other)!=Vector:
            raise TypeError
        return self.magnitude()>other.magnitude()
    
    def __len__(self):
        return 3
    
    def __getitem__(self,ind):
        if ind==0:
            return self.x
        elif ind==1:
            return self.y
        elif ind==2:
            return self.z
        else:
            raise ValueError
    
    def __eq__(self,other):
        if type(other)!=type(self):
            return False
        if len(self)!=len(other):
            return False
        c=0
        l=len(self)
        while c < l:
            if self[c]!=other[c]:
                return False
            c+=1
       
        return True
    
    def angle_to_other(self,other):
        """the angle between two vectors
        
        in radians
        
        """
        if type(other)!=type(self):
            raise TypeError
        

        v1=self
        v2=other
        
        m1=round(v1.magnitude(),3)
        m2=round(v2.magnitude(),3)
        
        try:
            v1=v1.copy()
            v2=v2.copy()
            v1=v1.normalize()
            v2=v2.normalize()
        except:
            print("vectors must be normalized, no methods give to support that")
            
        ang=math.acos((v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]))
        return ang
    
    
    def subs(self,d=None):
        raise NotImplemented
        #n_exprs=[]
        #for expr in self:
            #try:
                #n_expr=expr.subs(d)
            ##int and float don't support subs, they would throw attribute errors
            #except AttributeError:
                #n_expr=expr
            #n_exprs.append(n_expr)
        #return Vector(*n_exprs)
    def copy(self):
        return Vector(self.x,self.y,self.z)
        
    def cross(self,other):
        new_x=self.y*other.z-self.z*other.y
        new_y=self.z*other.x-self.x*other.z
        new_z=self.x*other.y-self.y*other.x
        return Vector(new_x,new_y,new_z)
        
    def __repr__(self):
        s=(self.x,self.y,self.z)
        s=str(s)
        return s
    
            
    def __neg__(self):
        return self.__mul__(-1)
    
    def __iter__(self):
        c=0
        while c <3:
            yield self[c]
            c+=1
    
    def __rtruediv__(self,quotient):
        raise TypeError("You can't devide through a vector") 
    
    def __ne__(self,other):
        return not self==other
    
    def __truediv__(self,quotient):
        l=[i/quotient for i in self]        
        return Vector(*l)
    
    def __round__(self,index):
        """round each entry"""
        return Vector(round(self[0],index),round(self[1],index),round(self[2],index))
        
    
    def __rmul__(self,other):
        return self*other
    
    def __mul__(self,other):
        """intended for multiplication of the vector with a scalar"""
        if isinstance(other,Vector):
            raise TypeError("use dot product instead")
        
        new_vals=[]
        for val in self:
            new_vals.append(val*other)
            
        return Vector(*new_vals)
    
        
    def __sub__(self,v2):
        
        if type(v2)==Vector:
            r=Vector(self[0]-v2[0],self[1]-v2[1],self[2]-v2[2])
            r=round(r,10)
            return r
        else:
            try:
                v2=Vector(*v2)
                r=Vector(self[0]-v2[0],self[1]-v2[1],self[2]-v2[2])
                r=round(r,10)
                return r
            except:
                raise TypeError
        
        
                
                
            
    
    def __add__(self,v2):
        return Vector(self[0]+v2[0],self[1]+v2[1],self[2]+v2[2])
    
    def dot(self,v2):
        v1=self
        return v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]
    
    def dyadic_polynom(self,v2):
        """
        as shown on
        https://en.wikipedia.org/wiki/Dyadic_tensor
        
        returns a polynom
        """
        s=0
        v1=self
        for val1 in v1:
            for val2 in v2:
                s+=val1*val2
        return s
        
    def outer_tensor_product(self,v2):
        """
        tensor product as shown on 
        https://en.wikipedia.org/wiki/Dyadic_tensor
        the function assumes the vectors are already in the appropriate base.
        
        returns a matrix
        """
        
        vectors=[]
        
        for val2 in v2:
            vs=[]
            for val1 in v1:
                vs.append(val1*val2)
                s+=val1*val2
            v=Vector(*vs)
            vectors.append(v)
        m=Matrix(*vectors)
        return m
    
    def set_magnitude(self,l):
        #ok so the issue is that magnitude is a derived property,
        #so actually I'm shortening the vector so the result will
        #be correct.
        
        v=self.copy()
        v=v*(l/self.magnitude())
        self.x=v.x
        self.y=v.y
        self.z=v.z
        
    def magnitude(self):
        v=self
        l=(v[0]**2+v[1]**2+v[2]**2)**0.5
        return l

    def normalize(self):
        v=self
        l=self.magnitude()
        return Vector(v[0]/l,v[1]/l,v[2]/l)

def angle_v1v2(v1,v2):
    """the angle between two vectors, in radians
    
    """
    
    val=(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])
    val=min(val,1)
    
        
    ang=math.acos(val)
    return ang
    
def get_radians_from_vector(x,y):
    angle=0
    if x>0:
        angle=math.atan(y/x)
    if x==0:
        angle=math.atan(y/0.001)
    if x<0:
        angle=math.atan(y/x)+math.pi
    if x>0 and y<=0:
        angle=math.atan(y/x)+math.pi*2
    if x==0 and y<=0:
        angle=math.atan(y/0.001)+math.pi*2
    return angle

def vector_interpolation_step(start,goal,step_size=1.5):
    goal=goal.copy()
    goal=goal.normalize()
    start=start.copy()
    start=start.normalize()
    
    rads1=get_radians_from_vector(start[0],start[1])
    rads2=get_radians_from_vector(goal[0],goal[1])
    
    #get difference between the vectors
    rads_diff=rads2-rads1
    
    #make sure to interpolate the shorter path
    if abs(rads_diff)>math.pi:
        sign=(rads_diff/abs(rads_diff))
        if sign>0:
            rads_diff=(math.pi*2)-abs(rads_diff)
            rads_diff=-rads_diff
        else:
            rads_diff=(math.pi*2)-abs(rads_diff)
            
    #if it's bigger than step, use the step
    #also go the right way.
    if abs(rads_diff)>step_size:
        if rads_diff >0:
            nrads_diff=step_size
        else:
            nrads_diff=-step_size
    else:
        nrads_diff=rads_diff
    
    #get the result.
    M=RotationMatrix(nrads_diff,Vector(0,0,1))
    result_vec=M*start
        
    return result_vec
