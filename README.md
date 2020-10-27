# vector

Another vector library? Yep.

I just wanted something where the operations I wanted where just there and not something I had to boilerplate again.

##advantages:

 * It's smaller than numpy.

 * You can probably tell what the code is doing by reading the code. Not to be underestimated.

 * it's straightforward, see:

import math
from vector import vector

v=vector.Vector(1,0,0)

z=vector.Vector(0,0,1)
m=vector.RotationMatrix(math.pi,z)

new=m*v
new
>>>(-1.0, 1.2246467991473532e-16, 0.0)
>>> round(new,3)
(-1.0, 0.0, 0.0)



