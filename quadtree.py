from p5 import *


class Point:
    def __init__(self, x, y, userData=None):
        self.x = x
        self.y = y
        self.userData = userData


class Area:
    def __init__(self, x1, y1, x2, y2):
        self.point1 = Point(x1, y1)
        self.point2 = Point(x2, y2)

    def intersects(self, point):
        top = point.y >= self.point1.y
        bottom = point.y < self.point2.y
        left = point.x >= self.point1.x
        right = point.x < self.point2.x

        return top and bottom and left and right

    def overlaps(self, area):
        return not (
            self.point1.x > area.point2.x
            or self.point2.x < area.point1.x
            or self.point1.y > area.point2.y
            or self.point2.y < area.point1.y
        )


class Quadtree:
    def __init__(self, nodeCapacity=1, boundry=Area(0, 0, width, height)):
        self.nodeCapacity = nodeCapacity
        self.boundry = boundry

        self.points = []

        self.northWest = None
        self.northEast = None
        self.southWest = None
        self.southEast = None

        self.subdivided = False

    def insert(self, point):
        if not (self.boundry.intersects(point)):
            return False

        if len(self.points) < self.nodeCapacity and not self.subdivided:
            self.points.append(point)
            return True

        if not self.subdivided:
            self.subdivide()
            self.subdivided = True

        if self.northWest.insert(point):
            return True

        if self.northEast.insert(point):
            return True

        if self.southWest.insert(point):
            return True

        if self.southEast.insert(point):
            return True

        return False

    def subdivide(self):
        x1 = self.boundry.point1.x
        x2 = (self.boundry.point2.x - x1) / 2 + x1
        x3 = self.boundry.point2.x

        y1 = self.boundry.point1.y
        y2 = (self.boundry.point2.y - y1) / 2 + y1
        y3 = self.boundry.point2.y

        nw = Area(x1, y1, x2, y2)
        ne = Area(x2, y1, x3, y2)
        sw = Area(x1, y2, x2, y3)
        se = Area(x2, y2, x3, y3)

        self.northWest = Quadtree(self.nodeCapacity, nw)
        self.northEast = Quadtree(self.nodeCapacity, ne)
        self.southWest = Quadtree(self.nodeCapacity, sw)
        self.southEast = Quadtree(self.nodeCapacity, se)

    def query(self, range):
        pointsInRange = []

        if not self.boundry.overlaps(range):
            return pointsInRange

        for point in self.points:
            if range.intersects(point):
                pointsInRange.append(point)

        if not self.subdivided:
            return pointsInRange

        pointsInRange = pointsInRange.concat(self.northWest.query(range))
        pointsInRange = pointsInRange.concat(self.northEast.query(range))
        pointsInRange = pointsInRange.concat(self.southWest.query(range))
        pointsInRange = pointsInRange.concat(self.southEast.query(range))

        return pointsInRange

    def show(self):
        line(
            self.boundry.point1.x,
            self.boundry.point1.y,
            self.boundry.point2.x,
            self.boundry.point1.y,
        )
        line(
            self.boundry.point1.x,
            self.boundry.point2.y,
            self.boundry.point2.x,
            self.boundry.point2.y,
        )
        line(
            self.boundry.point1.x,
            self.boundry.point1.y,
            self.boundry.point1.x,
            self.boundry.point2.y,
        )
        line(
            self.boundry.point2.x,
            self.boundry.point1.y,
            self.boundry.point2.x,
            self.boundry.point2.y,
        )
        if self.subdivided:
            self.northEast.show()
            self.northWest.show()
            self.southEast.show()
            self.southWest.show()
