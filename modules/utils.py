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


def cubeToAxial(x, y, z):
    q = x
    r = z

    return q, r


def axialToCube(q, r):
    x = q
    z = r
    y = -x-z

    return x, y, z

def cubeToOddQ(x, y, z):
    col = x
    row = z + (x - (x & 1)) / 2

    return int(col), int(row)
