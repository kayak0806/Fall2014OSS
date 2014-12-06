# EPPLER 379 AIRFOIL
# http://airfoiltools.com/airfoil/details?airfoil=e379-il
# rynold's number: ~200,000
# http://airfoiltools.com/calculator/reynoldsnumber
# keel:
# http://airfoiltools.com/polar/details?polar=xf-naca0006-il-100000

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import math
import pickle

class Boat(object):
    def __init__(self,main_sail):
        self.main_sail = main_sail
        self.mass = 54
        self.vel = Vector(2,0, polar=True)
        self.sail_coef = pickle.load(open("coefficients.p",'r'))
        self.keel_coef = pickle.load(open("keel_coefficients.py",'r'))

    def get_force(self,wind):
        AoA = self.get_AoA(wind)
        sail_lift = self.sail_lift(wind,AoA)
        sail_drag = self.sail_drag(wind,AoA)
        keel_lift = self.keel_lift(5)
        net_force = sail_lift + sail_drag + keel_lift
        return net_force
    def sail_lift(self, wind, AoA = 45):
        # L = 1/2 pressure (wind velocity)^2 area Cl
        windspeed = wind[0]
        p = 1.225  # kg/m^3
        A = 6.968  # m^2 (for sunfish)
        Cl = self.get_sail_coef(AoA)[0]
        lift = (0.5)*p*A*Cl*windspeed**2
        return Vector(lift, AoA,polar=True)
    def sail_drag(self, wind, AoA = 45):
        # D = 1/2 pressure (wind velocity)^2 area Cd
        windspeed = wind[0]
        p = 1.225  # kg/m^3
        A = 6.968  # m^2 (for sunfish)
        Cd = self.get_sail_coef(AoA)[1]
        drag = (0.5)*p*A*Cd*windspeed**2
        return Vector(drag,(270+AoA),polar=True)
    def keel_lift(self,speed):
        # L = 1/2 pressure (water velocity)^2 area Cl
        # TODO
        p = 0
        A = 0
        AoA = 0 # diff b/w boat vel dir and boat dir
        Cl = self.get_keel_coef(AOA)[0]
        lift = (0.5)*p*A*Cl*waterspeed**2
        return Vector(0,0)

    def get_sail_coef(self,alpha):
        # alpha is between -8 and 12
        # returns (C_lift,C_drag)
        alphas = sorted(self.sail_coef.keys())
        closest = min(alphas, key=lambda x:abs(x-alpha))
        return self.sail_coef[closest]
    def get_keel_coef(self,alpha):
    	alphas = sorted(self.keel_coef.keys())
    	closest = min(alphas, key=lambda x:abs(x-alpha))
    	return self.keel_coef[closest]

    def get_AoA(self,wind):
        return wind[1] - (self.main_sail+90)

    def set_sail(self,angle):
        # must be 0 to 90
        if angle<=90 and angle>=0:
            self.main_sail = angle
        else:
            print "Incorrect sail angle"

    def __str__(self):
        return "Main sail set to %d degrees"%self.main_sail

class Vector(object):
    def __init__(self,a,b, polar=False):
        if polar:
            # a = radius, b = angle in degrees
            self.x = a*math.cos(math.radians(b))
            self.y = a*math.sin(math.radians(b))
        else:
            self.x = a
            self.y = b
    def set_rect(self,x,y):
        self.x = x
        self.y = y
    def set_polar(self,r,th):
        self.x = r*math.cos(th)
        self.y = r*math.sin(th)
    def magnitude(self):
        return (self.x**2+self.y**2)**0.5
    def angle(self):
        return math.atan2(self.y,self.x)
    def get_vector(self):
        return np.array([self.x,self.y])
    def get_polar(self):
        r = (self.x**2 + self.y**2)**0.5
        a = math.atan2(self.y,self.x)
        return r,a
    def __str__(self):
        r,a = self.get_polar()
        return "(%g,%g)\nmagnitude: %g \nangle: %g"%(self.x,self.y,r,a)
    def __add__(a,b):
        x = a.x+b.x
        y = a.y+b.y
        return Vector(x,y)

def get_wind(mag,angle):
    '''if wind is accross starboard bow, 
        switch to port case'''
    if angle<90:
        angle = -1*angle+180
    elif angle>270:
        angle = -1*angle+540
    return mag,angle

def find_AoA(boat,wind):
    '''Choose the AoA that maximizes force magnitude'''
    forces = []
    max_force = (boat.get_force(wind),0)
    for angle in range(90):
        boat.set_sail(angle)
        force = boat.get_force(wind)
        # print force.magnitude(), max_force[0].magnitude()
        if force.magnitude()>max_force[0].magnitude():
            max_force = (force, angle)
    boat.set_sail(max_force[1])

def plot_wind(angles,fmag,fang):
    plt.plot(angles,fmag,'ro')
    # plt.plot(angles,fang,'bo')
    # plt.xlim([90,270])
    plt.show()

bert = Boat(45)
wind = get_wind(10,130)

# TEst
angles = []
fmag = []
fang = []
for i in range(180):
    angle = i+100
    wind = get_wind(10,angle)
    find_AoA(bert,wind)
    angles.append(wind[1])
    fmag.append(bert.get_force(wind).magnitude())
    fang.append(bert.get_force(wind).angle())
    print "--------------"
    # print "wind %d m/s at %d degrees"%wind
    # print bert.get_sail_coef(wind[1])
    print bert.get_force(wind)
plot_wind(angles,fmag,fang)




