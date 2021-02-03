from p5 import *
import quadtree as qt
from random import randint as ri

pointCount = 100

points = []


def setup():
    size(400, 400)
    for i in range(pointCount):
        points.append(qt.Point(ri(0, width), ri(0, height)))


def draw():
    background(120)
    stroke(255)
    stroke_weight(5)
    tree = qt.Quadtree()
    for p in points:
        tree.insert(p)
        point(p.x, p.y)

    stroke(100)
    stroke_weight(2)
    tree.show()


run()
