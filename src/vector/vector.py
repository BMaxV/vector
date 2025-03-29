
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
    
    def __eq__(self,other):
        
        if type(other)!=type(self):
            return False
        
        v1_ok = (self.v1 == other.v1)
        v2_ok = (self.v2 == other.v2)
        v3_ok = (self.v3 == other.v3)
        
        return all([v1_ok,v2_ok,v3_ok])
    
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
        s="["
        s+=f"{self.v1}\n"
        s+=f"{self.v2}\n"
        s+=f"{self.v3}]\n"
        return s
    
    def __mul__(self,other):
        
        if isinstance(other,Matrix):
            
            v1 = self * other.v1
            v2 = self * other.v2
            v3 = self * other.v3
            
            #v1 = self * Vector(other.v1.x,other.v2.x,other.v3.x)
            #v2 = self * Vector(other.v1.y,other.v2.y,other.v3.y)
            #v3 = self * Vector(other.v1.z,other.v2.z,other.v3.z)
            
            new_vs = [v1,v2,v3]
            M = Matrix(*new_vs)
            
            return M
            
        elif isinstance(other,Vector):
        
            i = 0
            j = 0
            new_values = []
            while i < 3:
                s = 0
                while j < 3:
                    # really? not j i, but i j and I missed this?
                    val1 = self[j][i]
                    val2 = other[j]
                    r = val1*val2
                    
                    #print(val1,val2,r)
                    s += r
                    j += 1
                
                new_values.append(s)
                
                j = 0
                i += 1
                
            V = Vector(*new_values)
            V = round(V,15)
            return V

        else:
            try:
                other2 = Vector(*other)
                r = self*other2
                return r
            except:
                raise TypeError("not a compatible object/type?"+str(type(other)))
                
    def from_Rotation(self,target,z):
        """ takes two vectors, rotation axis is calculated as cross product
        then rotation is applied as acos of the dot product"""
        
        rot_axis=target.cross(z)
        angle=math.acos(target.dot(z))
        M=self.Rotation(angle,None,rot_axis)
        
        return M

def get_normal_tangent_for_sphere_point(point):
    normal = point.normalize()
    
    up = Vector(0,0,1)
    
    default_tangent = point.cross(up)
    default_tangent = default_tangent.normalize()
    
    
    return normal, default_tangent

def get_sphere_point_local_vector_matrices(sphere_point,local_rotation,base_vector=(0,1,0)):
    """
    returns two matrices, one rotates a point from a "default" orientation into a sphere position with the local rotation applied.
    the other rotates from the sphere point to the default orientation, applies the local rotation and rotates back
    
    e.g.  a local movement vector with an indicator or vector object that is being created in the default orientation.
    
    """
    up = Vector(0,0,1)
    
    point_normal, org_tangent = get_normal_tangent_for_sphere_point(sphere_point)
    
    # this tagent, even if I rotate it up, has some amount of rotation applied to it.
    # because it's orthogonal to both up and my position point.
    
    matrix, angle, axis  = get_rotation_data(sphere_point, up)
    up_rot_matrix = RotationMatrix(angle, axis)
    
    base_indicator_vector = Vector(*base_vector)
    tangent_2d = up_rot_matrix * org_tangent
    
    # this is the angle difference between my default orientation
    # and the angle of my sphere point vector that is due to 
    # the sphere point not being on the 0 meridian.
    
    offset_angle = angle_v1v2(base_indicator_vector,tangent_2d)
    
    # can only detect the angle magnitude but not the direction
    # directly, so I have try and find which one makes sense.
    flat_rot_1 = RotationMatrix(offset_angle, up)
    flat_rot_2 = RotationMatrix(-offset_angle, up)
    if round((flat_rot_1*base_indicator_vector).dot(tangent_2d),4)==1:
        
        offset = flat_rot_1
    else:
        this = round((flat_rot_2*base_indicator_vector).dot(tangent_2d),4)
        assert this == 1
        offset = flat_rot_2
    
    flat_rot = RotationMatrix(local_rotation, up)
    
    down_rot_matrix = RotationMatrix(-angle, axis)
    
    # THIS is for my indicator, which starts at some rotation up top.
    # like, my default points to +x or +y or something.
    indicator_matrix = down_rot_matrix * flat_rot * offset
    
    # THIS STUFF is for my plate vector which is any other kind of
    # orientation, but
    point_change_matrix = down_rot_matrix * flat_rot * up_rot_matrix
    
    return indicator_matrix, point_change_matrix


def get_rotation_data(from_v,to_v):
    """
    assuming that p2 is "up" this returns the matrix, angle and axis
    for rotating towards that state.
    
    returns a matrix, angle and axis,

    to revert the rotation from the matrix, make a new
    one with (-ang, axis)
    """
        
    from_v = from_v.normalize()
    to_v = to_v.normalize()
    
    rot_axis = from_v.cross(to_v)
    rot_axis = rot_axis.normalize()
    # give me the angle.
    angle = angle_v1v2(from_v,to_v)
    
    # these are the matrices I will rotate everything with later.
    RMx = RotationMatrix(angle,rot_axis)
    
    return RMx, angle, rot_axis

def get_face_normal(vertlist):
    """assuming the face is coplanar"""
    
    center = Vector(0,0,0)
    for x in vertlist:
        center += x
    center = center / len(vertlist)
    
    c = -1
    m = len(vertlist)
    norms = []
    while c < m-1:
        
        vx1 = vertlist[c]
        vx2 = vertlist[c+1]
        
        vv1 = center - vx1
        vv2 = center - vx2
        
        vv1 = vv1.normalize()
        vv2 = vv2.normalize()
        
        norm = vv1.cross(vv2)
        norm = norm.normalize()
        norms.append(norm)
        c += 1
    
    real_norm = Vector(0,0,0)
    for t_norm in norms:
        real_norm += t_norm
        
    real_norm = real_norm / len(norms)
    real_norm = real_norm.normalize()
    assert real_norm.magnitude() != 0
    
    #print(norm)
    #print(vv1,vv2)
    
    # try:
        # for x in vertlist:
            # val = norm.dot(x)
            # assert val == 0
            
    # except AssertionError:
        # raise ValueError("dot product isn't 0, vertlist is not coplanar.")
        
    return real_norm
    
def get_edge_normals(vertlist):
    """
    """
    
    norm = get_face_normal(vertlist)
    rm = RotationMatrix(math.pi/2, norm)
    
    edge_normals = []
    c = -1
    m = len(vertlist)
    all_lower = True
    while c < m-1:
        v1 = vertlist[c]
        v2 = vertlist[c+1]
        vec = (v1-v2)
        edge_normal = rm * vec # this might have to turn the other way.
        edge_normal = edge_normal.normalize()
        edge_normals.append(edge_normal)
        c += 1
    this = edge_normals.pop(0)
    edge_normals.append(this)
        
    return edge_normals

def get_faked_3d_point_inside(vertlist,point):
    """this is not entirely accurate,
    I'm interpreting the vert list as defining a prism,
    I'm assuming all points are coplanar and sorted.
    I take the edge normal and check whether the vector from
    an edge point to "point" is less than 0
    
    if that's consistent for all edges, the point is inside.
    """
    
    normals = get_edge_normals(vertlist)
    all_lower = True
    all_higher = True
    c = -1
    m = len(vertlist)
    
    while c < m:
        
        edge_normal = normals[c]
        v1 = vertlist[c]
        vec = (point-v1)
        dot_val = vec.dot(edge_normal)
        if dot_val > 0:
            all_lower = False
        if dot_val < 0:
            all_higher = False
        
        c += 1
    if all_higher and all_lower:
        return False # error
    elif all_higher and not all_lower:
        return True
    elif all_lower and not all_higher:
        return True
    else:
        # regular case where it's outside
        return False 
    
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
    
    #oh yeah, straight copied this from wikipedia, just have to get it right.
    v1=Vector(t*x**2+c  ,t*x*y+z*s, t*x*z-y*s)
    v2=Vector(t*x*y-z*s ,t*y**2+c,  t*y*z+x*s)
    v3=Vector(t*x*z+y*s ,t*y*z-x*s, t*z**2+c)
    
    M=Matrix(round(v1,6),round(v2,6),round(v3,6))
    return M

class Vector:
    
    def __init__(self,x,y,z,force_convert_simple_type=False):
        """
        Works basically like a list or a tuple, except it supports
        common vector funtions.
        """
        
        #duck type check
        1+x,1+y,1+z
        
        self.x = x 
        self.y = y 
        self.z = z 
        
        if force_convert_simple_type:
            self.x=float(x)
            self.y=float(y)
            self.z=float(z)
    
    
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
        if ind == 0:
            return self.x
        elif ind == 1:
            return self.y
        elif ind == 2:
            return self.z
        else:
            raise ValueError
    
    def __eq__(self,other):
        
        if type(other) not in [tuple,list,type(self)]:
            #this should... take care of type problems.
            
            # don't be that agressive, 
            # I want to be able to do vector == None -> False
            # raise TypeError
            
            return False
            
        if len(self)!=len(other):
            return False
        
        c = 0
        l = len(self)
        while c < l:
            if self[c] != other[c]:
                return False
            c += 1
       
        return True
    
    def angle_to_other(self,other):
        """
        the angle between two vectors
        
        in radians
        """
        if type(other)!=type(self):
            raise TypeError("inputs aren't both vectors.")
        
        v1 = self
        v2 = other
        
        if v1.magnitude() == 0:
           raise ValueError("this vector has no length") 
        if v2.magnitude() == 0:
            raise ValueError("the other vector has no length")
            
        
        try:
            v1 = v1.copy()
            v2 = v2.copy()
            v1 = v1.normalize()
            v2 = v2.normalize()
        except:
            print("vectors must be normalized, no methods give to support that")
        
        # floating point nonsense.
        value = (v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])
        if not (-1 <= value <= 1):
            value = round(value,8) 
        ang = math.acos(value)
        
        return ang
    
    def to_string(self):
        s = "("+",".join([str(self.x),str(self.y),str(self.z)])+")"
        return s
    
    @classmethod
    def from_string(self,s):
        s=s.strip("(")
        s=s.strip(")")
        s=s.split(",")
        tup=[float(x) for x in s]
        return Vector(*tup)
    
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
        r=Vector(self[0]-v2[0],self[1]-v2[1],self[2]-v2[2])
        r=round(r,10)
        return r
        
    def __add__(self,v2):
        v = Vector(self[0]+v2[0],self[1]+v2[1],self[2]+v2[2])
        v = round(v,10)
        return v
    
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
        v = self
        l = (v[0]**2+v[1]**2+v[2]**2)**0.5
        return l
    
    def normalize(self):
        v = self
        l = self.magnitude()
        if l == 0:
            return Vector(0,0,0)
        return Vector(v[0]/l,v[1]/l,v[2]/l)
    
    def get_absolute_radians(self):
        value = get_radians_from_vector(self.x,self.y)
        return value
    
def angle_v1v2(v1,v2):
    """the angle between two vectors, in radians
    
    """
    v1=v1.normalize()
    v2=v2.normalize()
    val=(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])
    val=min(val,1)
    
        
    ang=math.acos(val)
    return ang
    
def get_radians_from_vector(x,y):
    angle=0
    if x>0:# and y>0:
        angle=math.atan(y/x)
    if x==0:
        angle=math.atan(y/0.001)
    if x<0:
        angle=math.atan(y/x)+math.pi
    if x > 0 and y <= 0:
        angle=math.atan(y/x)
    if x == 0 and y <= 0:
        angle=math.atan(y/0.001)+math.pi
    return angle

def vector_sum(my_iterable):
    sum_ob = Vector(0,0,0)
    for thing in my_iterable:
        sum_ob +=thing
    return sum_ob
    
def vector_interpolation_step(start,goal,step_size=1.5):
    goal = goal.copy()
    goal = goal.normalize()
    start = start.copy()
    start = start.normalize()
    
    rads1 = get_radians_from_vector(start[0],start[1])
    rads2 = get_radians_from_vector(goal[0],goal[1])
    
    # get difference between the vectors
    rads_diff = rads2-rads1
    #print(rads_diff)
    # make sure to interpolate the shorter path
    if abs(rads_diff) > math.pi:
        sign = (rads_diff/abs(rads_diff))
        if sign > 0:
            rads_diff = (math.pi*2)-abs(rads_diff)
            rads_diff = -rads_diff
        else:
            rads_diff = (math.pi*2)-abs(rads_diff)
            
    #if it's bigger than step, use the step
    #also go the right way.
    if abs(rads_diff) > step_size:
        if rads_diff > 0:
            nrads_diff = step_size
        else:
            nrads_diff = -step_size
    else:
        nrads_diff = rads_diff
    
    # get the result.
    M = RotationMatrix(nrads_diff,Vector(0,0,1))
    result_vec = M*start
        
    return result_vec, rads_diff
