from math import sin, cos
"""
这是一个求圆形极角坐标的函数
"""
Pi = 3.14159265358979323846264338327950288  # 圆周率


def polar_angle_x(x, r, angle):
    return x + r * cos(angle * Pi / 180)


def polar_angle_y(y, r, angle):
    return y + r * sin(angle * Pi / 180)
