# See sources.txt for info on sail and keel airfoils

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import math
import pickle

class Boat(object):
    def __init__(self,main_sail):
        self.main_sail = main_sail
        self.boat_angl = 0
        self.mass = 54
        self.vel = Vector(2,0, polar=True)
        self.sail_coef = pickle.load(open("coefficients.p",'r'))
        self.keel_coef = pickle.load(open("keel_coefficients.p",'r'))

    def get_force(self,wind):
        windAoA = self.get_wind_AoA(wind)
        keelAoA = self.get_keel_AoA(wind)
        sail_lift = self.sail_lift(wind,windAoA)
        sail_drag = self.sail_drag(wind,windAoA)
        # keel_lift = self.keel_lift(5.0,keelAoA)
        # keel_drag = self.keel_drag(5.0, keelAoA)
        net_force = sail_lift + sail_drag #+ keel_lift +keel_drag
        return net_force
    def sail_lift(self, wind, AoA = 45):
        # L = 1/2 density (wind velocity)^2 area Cl
        windspeed = wind[0]
        p = 1.225  # kg/m^3
        A = 6.968  # m^2 (for sunfish)
        Cl = self.get_sail_coef(AoA)[0]
        lift = (0.5)*p*A*Cl*windspeed**2
        return Vector(lift, self.main_sail,polar=True)
    def sail_drag(self, wind, AoA = 45):
        # D = 1/2 density (wind velocity)^2 area Cd
        windspeed = wind[0]
        p = 1.225  # kg/m^3
        A = 6.968  # m^2 (for sunfish)
        Cd = self.get_sail_coef(AoA)[1]
        drag = (0.5)*p*A*Cd*windspeed**2
        return Vector(drag,(270+self.main_sail),polar=True)
    def keel_lift(self,speed,AoA):
        # L = 1/2 density (water velocity)^2 area Cl
        # TODO
        waterspeed = speed[0];
        p = 1020  # kg/m^3
        A = 0.249 # m^2. sunfish daggerboard dimentions.
        Cl = self.get_keel_coef(AoA)[0]
        lift = (0.5)*p*A*Cl*waterspeed**2
        return Vector(lift, 180-AoA,polar=True)
    def keel_drag(self,speed,AoA):
        # L = 1/2 density (water velocity)^2 area Cl
        # TODO
        waterspeed = speed[0];
        p = 1020  # kg/m^3
        A = 0.249 # m^2. sunfish daggerboard dimentions.
        Cd = self.get_keel_coef(AoA)[1]
        drag = (0.5)*p*A*Cd*waterspeed**2
        return Vector(drag, 270-AoA,polar=True)

    def get_sail_coef(self,alpha):
        # alpha is between -8 and 12
        # returns (C_lift,C_drag)
        if alpha < -8 or alpha >12:
            return (0,0)
        alphas = sorted(self.sail_coef.keys())
        closest = min(alphas, key=lambda x:abs(x-alpha))
        return self.sail_coef[closest]
    def get_keel_coef(self,alpha):
    	alphas = sorted(self.keel_coef.keys())
    	closest = min(alphas, key=lambda x:abs(x-alpha))
    	return self.keel_coef[closest]

    def get_wind_AoA(self,wind):
    	alpha =(self.main_sail+90) - wind[1] 
        return alpha
    def get_keel_AoA(self,wind):
        windAoA = self.get_wind_AoA(wind)
        liftx = self.sail_lift(wind,windAoA).x
        dragx = self.sail_drag(wind,windAoA).x
        sailX = liftx + dragx
        aRange = [a for a in sorted(self.keel_coef.keys()) if a>0]
        force_dif = []
        for a in aRange:
            kliftx = self.keel_lift((5.0,1),a).x
            kdragx = self.keel_drag((5,1),a).x
            keelX = kliftx + kdragx
            force_dif.append( (keelX-sailX,a) )
        return min(force_dif)[1]

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
        return "(%g, %g)\nmagnitude: %g\nangle: %g"%(self.x,self.y,r,a)
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

def find_sail_angle(boat,wind):
    '''Choose the AoA that maximizes force magnitude'''
    forces = []
    max_force = (boat.get_force(wind),0)
    for angle in range(90):
        boat.set_sail(angle)
        force = boat.get_force(wind)
        if force.magnitude()>max_force[0].magnitude():
            max_force = (force, angle)
    boat.set_sail(max_force[1])

def plot_wind(angles,fmag,fang):
    plt.plot(angles,fmag,'g')
    plt.plot(angles,fang,'b')
    # plt.xlim([95,265])
    plt.show()

bert = Boat(45)
wind = get_wind(10,95)

find_sail_angle(bert,wind)
print bert




