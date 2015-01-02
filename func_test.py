import matplotlib.pyplot as plt

import sim1 as s


def plotter(angles, numbers):
    plt.plot(angles,numbers)
    plt.show()

def test_wind():
    windy = []
    for i in range(360):
        windy.append(s.get_wind(10,i)[1])
    plotter(range(360),windy,windy)

ernie = s.Boat(45)
def test_AoA_wind():
    for j in range(90/5): # 0 at S, 90 at E
        j*=5
        ernie.set_sail(j)
        attack = []
        wind = [w*10+90 for w in range(180/10)]
        for w in wind: # 90 to 270
            e = ernie.get_wind_AoA( (0,w) )
            attack.append(e)
        plt.plot(wind,attack)
    plt.show()

def test_sail_lift():
    # check alphas (<-8,>-8,<12,>12)
    # cycle through wind angles (90,270, 20)
    # cycle through wind magnitudes (0,10,0.5)
    # result: a Vector (show mag and dir)
    alphas = [a-9 for a in range(23)]
    high_mags = []
    high_angs = []
    for a in alphas:
        mags=[]
        angs=[]
        winds = [m*0.5 for m in range(10)]
        for w in winds:
            wind = w,0
            lift = ernie.sail_lift(wind,a)
            mags.append(lift.magnitude())
            angs.append(lift.angle())
        high_mags.append(mags[-1])
        high_angs.append(angs[-1])
        plt.subplot(2,2,1)
        plt.plot(winds,mags,'-')
        plt.subplot(2,2,2)
        plt.plot(winds,angs,'.-')
    plt.subplot(2,2,3)
    plt.plot(alphas,high_mags,'.-')
    plt.subplot(2,2,4)
    plt.plot(alphas,high_angs,'.-')
    plt.show()

def test_sail_drag():
    # cycle through angle of attacks
    # cycle through wind magnitudes (0,10,0.5)
    # plots: lift/wind magnitude & lift/AoA for mag and angl
    alphas = [a-9 for a in range(23)]
    high_drags = []
    for a in alphas:
        drags=[]
        mags = [m*0.5 for m in range(10)]
        for mag in mags:
            wind = mag,0
            drag = ernie.sail_drag(wind,a)
            drags.append(drag.magnitude())
        high_drags.append(drags[-1])
        plt.subplot(1,2,1)
        plt.plot(mags,drags,'-')
    plt.subplot(1,2,2)
    plt.plot(alphas,high_drags,'.-')
    plt.show()

def test_keel_lift():
    # check alphas (<-8,>-8,<12,>12)
    # cycle through wind angles (90,270, 20)
    # cycle through wind magnitudes (0,10,0.5)
    # result: a Vector (show mag and dir)
    alphas = [a-11 for a in range(23)]
    high_lifts = []
    for a in alphas:
        lifts=[]
        mags = [m*0.5 for m in range(10)]
        for mag in mags:
            wind = mag,0
            lift = ernie.keel_lift(wind,a)
            lifts.append(lift.magnitude())
        high_lifts.append(lifts[-1])
        plt.subplot(1,2,1)
        plt.plot(mags,lifts,'-')
    plt.subplot(1,2,2)
    plt.plot(alphas,high_lifts,'.-')
    plt.show()

def test_keel_drag():
    # check alphas (<-8,>-8,<12,>12)
    # cycle through wind angles (90,270, 20)
    # cycle through wind magnitudes (0,10,0.5)
    # result: a Vector (show mag and dir)
    alphas = [a-11 for a in range(23)]
    mags = [m*0.5 for m in range(10)]
    high_drags = []
    for a in alphas:
        drags=[]
        for mag in mags:
            wind = mag,0
            drag = ernie.keel_drag(wind,a)
            drags.append(drag.magnitude())
        high_drags.append(drags[-1])
        plt.subplot(1,2,1)
        plt.plot(mags,drags,'-')
    plt.subplot(1,2,2)
    plt.plot(alphas,high_drags,'.-')
    plt.show()



def test_AoA_keel():
    ernie.set_sail(45)
    wind_magnitudes = [m*0.5 for m in range(10)]
    wind_angles = [w*0.5+130 for w in range(20)]
    for m in wind_magnitudes: # 90 to 270
        alphas = []
        for w in wind_angles:
            e = ernie.get_keel_AoA( (m,w) )
            alphas.append(e)
        plt.plot(wind_angles,alphas)
    plt.show()

def test_coef_sail():
    for a in range(90):
        a -=45
        (l,d) = ernie.get_sail_coef(a)
def test_coef_keel():
    alphas = [a-45 for a in range(90)]
    lifts = []
    drags = []
    for a in alphas:
        (l,d) = ernie.get_keel_coef(a)
        lifts.append(l)
        drags.append(d)
    plt.subplot(121)
    plt.plot(alphas,lifts)
    plt.subplot(122)
    plt.plot(alphas,drags)
    plt.show()

def test_final():
    ernie.set_sail(0)
    magnitudes = [a for a in range(10)]
    angles = [a*10+90 for a in range(180/10)]
    for m in magnitudes:
        print m
        sail = []
        for a in angles:
            wind = (m,a)
            s.find_sail_angle(ernie,wind)
            sail.append(ernie.main_sail)
        plt.plot(angles,sail,'.-')
    plt.xlabel('wind angle', fontsize=14, color='red')
    plt.ylabel('sail angle', fontsize=14, color='red')
    plt.show()





# test_wind()
# test_AoA_wind()
'''test_AoA_keel()'''
# test_coef_sail()
# test_coef_keel()
# test_sail_lift()
# test_sail_drag()
# test_keel_lift()
# test_keel_drag()

test_final()