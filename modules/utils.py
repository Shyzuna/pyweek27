cubeDirections = [
    (+1, -1, 0), (+1, 0, -1), (0, +1, -1),
    (-1, +1, 0), (-1, 0, +1), (0, -1, +1)
]

def hexRound(q, r):
    x, y, z = axialToCube(q, r)
    rx, ry, rz = cubeRound(x, y, z)
    nq, nr = cubeToAxial(rx, ry, rz)

    return nq, nr


def cubeRound(x, y, z):
    rx = round(x)
    ry = round(y)
    rz = round(z)

    x_diff = abs(rx - x)
    y_diff = abs(ry - y)
    z_diff = abs(rz - z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry

    return rx, ry, rz


def cubeScale(x, y, z, s):
    return s*x, s*y, s*z


def cubeNeighbour(x1, y1, z1, i):
    x2, y2, z2 = cubeDirections[i]
    return cubeAdd(x1, y1, z1, x2, y2, z2)


def cubeAdd(x1, y1, z1, x2, y2, z2):
    return x1+x2, y1+y2, z1+z2


def cubeRing(x, y, z, radius):
    results = []
    a, b, c = cubeDirections[4]
    sx, sy, sz = cubeScale(a, b, c, radius)
    ax, ay, az = cubeAdd(x, y, z, sx, sy, sz)

    for i in range(6):
        for j in range(radius):
            results.append((ax, ay, az))
            ax, ay, az = cubeNeighbour(ax, ay, az, i)


    return results


def cubeSpiral(x, y, z, radius):
    # /!\ ne contient pas le centre dans les resultats
    results = []

    for i in range(1, radius+1):
        results += cubeRing(x, y, z, i)

    return results


def cubeToAxial(x, y, z):
    q = x
    r = z

    return q, r


def cubeToOddQ(x, y, z):
    col = x
    row = z + (x - (x & 1)) / 2

    return int(col), int(row)


def axialToCube(q, r):
    x = q
    z = r
    y = -x-z

    return x, y, z


def oddQToCube(q, r):
    x = q
    z = r - (q - (q & 1)) / 2
    y = -x-z
    return x, y, z


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def cubeDistance(x1, y1, z1, x2, y2, z2):
    return max(abs(x1-x2), abs(y1-y2), abs(z1-z2))


def lerp(a, b, t):
    return a + (b - a)*t


def cubeLerp(x1, y1, z1, x2, y2, z2, t):
    return lerp(x1, x2, t), lerp(y1, y2, t), lerp(z1, z2, t)


def cubeLineDraw(x1, y1, z1, x2, y2, z2):
    dist = cubeDistance(x1, y1, z1, x2, y2, z2)
    results = []

    for i in range(int(dist) + 1):
        x, y, z = cubeLerp(x1, y1, z1, x2, y2, z2, i/dist)
        results.append(cubeRound(x, y, z))

    return results