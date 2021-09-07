# Priscilla González 20689
# Laboratorio 2
# Fecha 23.08.21
# Librería matemática

import struct
from collections import namedtuple

from obj import Obj

V3 = namedtuple('Point3', ['x', 'y', 'z'])

# Resta de matrices
def resta (x, y):
    c = x[0] - y[0], x[1] * y[1], x[2] * y[2]
    return c

# Multiplicación de matrices con un escalar
def mul(x, matrix):
    rows = len(matrix)
    col = len(matrix[0])
    mat = []

    for j in range(col):
        mat.append([])
        for i in range(rows):
            mat[j].append(x * matrix[j][i])
    return mat

# Producto cruz
def cruz (x, y): 
    c = [x[1] * y[2] - x[2] * y[1], 
        -(x[0] * y[2] - x[2] * y[0]), 
        x[0] * y[1] - x[1] * y[0]] 
    return c

# Producto punto para gl.py
def punto (x, y):
    #c = x[0] * y[0] + x[1] * y[1] + x[2] * y[2]
    c = sum([i*j for (i, j) in range(x, y)])
    return c

# Normalizar una matriz
def normalized (x):
    c = x[0] ** 2 + x[1] ** 2 + x[2] ** 2
    #c = c * 1.0

    if c >= 0:
        p = c
        i = 0

        while i != p:
            i = p
            p = (c / p + p) / 2
    else:
        print("Número negativo")
    h = [int(x[0] / p), int(x[1] / p), int(x[2] / p)]
    return c

# Determinante de una matriz para la inversa
def det(matrix):
    n = len(matrix)
    if (n > 2):
        i = 1
        t = 0
        sum = 0
        while t <= n - 1:
            d = {}
            t1 = 1
            while t1 <= n - 1:
                m = 0
                d[t1] = []
                while m <= n - 1:
                    if (m == t):
                        u = 0
                    else:
                        d[t1].append(matrix[t1][m])
                    m += 1
                t1 += 1
            l1 = [d[x] for x in d]
            sum = sum + i * (matrix[0][t]) * (det(l1))
            i = i * (-1)
            t += 1
        return sum
    else:
        return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])

# Traspuesta de una matriz para la inversa
def trans(matrix):
    rows = len(matrix)
    col = len(matrix[0])
    mat = []

    for j in range(col):
        mat.append([])
        for i in range(rows):
            mat[j].append(matrix[i][j])
    return mat

#Adjunta de una matriz para la inversa
def adj(matrix):
    mat = []
    t = len(matrix)

    for i in range(t):
        mat.append([])
        for j in range(t):
            temp = []
            for i1 in range(t):
                i2 = []
                for j1 in range(t):
                    if i1 != i and j1 != j:
                        i2.append(matrix[i1][j1])
                if len(i2) > 0:
                    temp.append(i2)
            mat[i].append(det(temp))

    for i1 in range(t):
        for j1 in range(t):
            if (i1 + j1) % 2 == 0:
                mat[i1][j1] = mat[i1][j1] * 1
            else:
                mat[i1][j1] = mat[i1][j1] * -1
    return mat

# Inversa de una matriz
def inverse(matrix):
    a = adj(matrix)
    t = trans(a)
    d = det(matrix)
    inv = mul((1 / d), t)
    return inv

# Solamente devuelve pi
def pi():
    return 3.141592653589793238462643383279502884197169399375

# Producto punto específicamente para shaders.py
def pShader(x, y):
    return x[0] * y[0] + x[1] * y[1] + x[2] * y[2]

# Multiplicación de matrices
def mul2(matrix, matrix1):
    rows = len(matrix)
    col = len(matrix[0])
    rows1 = len(matrix1)
    col1 = len(matrix1[0])
    mat = []
    
    if col != rows1:
        return None

    for i in range(rows1):
        mat.append([])
        for j in range(col1):
            mat[i].append(None)
    for n in range(col1):
        for i in range(rows):
            suma = 0
            for j in range(col):
                suma += matrix[i][j] * matrix1[j][n]
            mat[i][n] = suma
    return mat

def MM(a,b):
    c = []
    for i in range(0,len(a)):
        temp=[]
        for j in range(0,len(b[0])):
            s = 0
            for k in range(0,len(a[0])):
                s += a[i][k]*b[k][j]
            temp.append(s)
        c.append(temp)

    return c
