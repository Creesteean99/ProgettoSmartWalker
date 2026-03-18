import math
from tf_transformations import quaternion_from_euler
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point

def make_point(x,y,z):
    pt = Point()
    pt.x = x
    pt.y = y
    pt.z = z
    return pt

def make_pose(x,y,theta):
    q = quaternion_from_euler(0, 0, math.radians(theta))
    posa = Pose()

    posa.position.x = x
    posa.position.y = y
    posa.position.z = 0.0

    posa.orientation.x = q[0]
    posa.orientation.y = q[1]
    posa.orientation.z = q[2]
    posa.orientation.w = q[3]

    return posa

# Pose Definition
HOME = make_pose(2.5,-2.1,90)
BED = make_pose(-3.5,-0.9,90)
COUCH = make_pose(3.15,-1.7,180)
TOILETTE = make_pose(-1.0,0.5,180)

# Guide's points definition
START_POINT = make_point(1.0,-2.0,0.0)
END_POINT = make_point(1.96,-1.34,0.0)

# Guide's line thickness
THICKNESS = 0.06