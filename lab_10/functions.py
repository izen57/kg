from math import cos, pi, sin

funcs = list()

funcs.append(lambda x, z: sin(x) * sin(z))
funcs.append(lambda x, z: sin(cos(x)) * sin(z))
funcs.append(lambda x, z: cos(x) * z / 3)