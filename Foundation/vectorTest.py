#!/usr/bin/python
# -*- coding: utf-8 -*-

from vector import *

v1 = Vector(1,2,3)
v2 = Vector(3,2,1)
v1 = v1*5

v3 = v1 + v2
print(v1)
print(v3)
print("Laenge V3 ",v3.get_length())
print("V3 normalisiert",v3.normalized())
print("V1 x V3",v1.cross(v3))
print("Winkel zwischen V1 und V3",v1.get_angle_between(v3))