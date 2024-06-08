import numpy as np
import math
import matplotlib.pyplot as plt
import random

def move(kesiI, v, w):
    x, y, teta = kesiI
    Vx = v
    Vy = 0
    omega = w
    kesiDotR = np.array([[Vx],
                         [Vy],
                         [omega]])
    RInverse = np.array([[math.cos(-teta), math.sin(-teta), 0],
                  [-math.sin(-teta), math.cos(-teta), 0],
                  [0, 0, 1]])
    kesiDotI = RInverse.dot(kesiDotR)
    newKesiI = np.array([(x + 0.05*kesiDotI[0])[0],
                         (y + 0.05*kesiDotI[1])[0],
                         (teta + 0.05*kesiDotI[2])[0]]).tolist()
    return newKesiI

def getAlpha(currentCoordinate):
    teta = currentCoordinate[2]
    f = math.atan2(0 - currentCoordinate[1], 0 - currentCoordinate[0])
    alpha = f - teta
    while alpha > math.pi:
        alpha -= 2 * math.pi
    while alpha < -math.pi:
        alpha += 2 * math.pi
    return alpha

def getBeta(teta, alpha):
    beta = -teta - alpha
    while beta > math.pi:
        beta -= 2 * math.pi
    while beta < -math.pi:
        beta += 2 * math.pi
    return beta

def getRo(currentCoordinate):
    return math.sqrt(currentCoordinate[0] ** 2 + currentCoordinate[1] ** 2)

def main(currentCoordinate):
    alpha = getAlpha(currentCoordinate)
    beta = getBeta(currentCoordinate[2], alpha)
    ro = getRo(currentCoordinate)

    if alpha <= math.pi/2 and alpha >= -math.pi/2:
            Kro = 1/10
            Kb = -1/10
            Ka = 2/10
    else:
            Kro = -1/10
            Kb = 1/10
            Ka = -2/10

    xValues=[]
    yValues=[]

    while True:

        xValues.append(currentCoordinate[0])
        yValues.append(currentCoordinate[1])
        v = Kro * ro
        w = Kb * beta + Ka * alpha
        currentCoordinate = move(currentCoordinate, v, w)
        alpha = getAlpha(currentCoordinate)
        beta = getBeta(currentCoordinate[2], alpha)
        ro = getRo(currentCoordinate)
        if alpha < 0.0001 and beta < 0.0001 and ro < 0.0001:
            break
    return xValues, yValues

if __name__ == '__main__':
    # Starting point configuration
    differentStarts = [[0, 0.5, 0], [0.5, 0, math.pi], [-0.35, -0.35, 0], [-0.5, 0, math.pi/2], [0.46, 0.2, math.pi], [-0.47, -0.18, 0], [-0.2, 0.46, 0]]
    colors = ['r', 'b', 'g', 'y', 'c', 'm', 'tab:pink', 'tab:gray', 'tab:brown', 'tab:orange', 'tab:olive']

    plt.figure()
    for startPoint in differentStarts:
        # Taken Path
        xValues, yValues = main(startPoint)
        plt.plot(xValues, yValues, colors[random.randint(0, 9)])

        # Expected Path
        x, y = startPoint[0], startPoint[1]
        if x > 0: 
            t = np.linspace(0.001, x, 400)
        else:
            t = np.linspace(x, 0.001, 400)
        f = (y / (x + 0.001)) * t
        plt.plot(t, f, '--k')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title("X-Y")
    plt.axis('equal')
    plt.show()