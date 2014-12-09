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
        print "----------- ",j+270
        ernie.set_sail(j)
        attack = []
        ws = []
        for i in range(180/10): # 90 to 270
            w = i*10+90
            ws.append(w)
            e = ernie.get_wind_AoA( (0,w) )
            attack.append(e)
            print w," : ",e
        plt.plot(ws,attack)
    plt.show()

def test_sail_lift():
    # cycle through alpha
    # cycle through wind angles
    # cycle through wind magnitudes
    # result: a Vector (show mag and dir)


def test_AoA_keel():
    attack = []
    ws = []
    for i in range(180/10): # 90 to 270
        w = i*10+90
        ws.append(w)
        e = ernie.get_keel_AoA( (0,w) )
    #     attack.append(e)
    # plt.plot(ws,attack)
    # plt.show()




# test_wind()
# test_AoA_wind()
'''test_AoA_keel()'''
test_sail_lift()

