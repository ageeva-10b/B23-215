from math import *


def area2(a, b, c):
    return abs(0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x)))


def min_dist(a, b, c):
    if dist2(a, b) < dist2(a, c):
        return b
    return c


def intersection_segment_circle(p1, p2, center, radius):
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    cx, cy = center.x, center.y

    dx = x2 - x1
    dy = y2 - y1
    if dx != 0:
        a = dx ** 2 + dy ** 2
        b = -2 * dx ** 2 * cx - 2 * dy ** 2 * x1 + \
            2 * dx * dy * (y1 - cy)
        c = cx ** 2 * dx ** 2 + dy ** 2 * x1 ** 2 - \
            2 * dx * (y1 - cy) * dy * x1 + dx ** 2 * (
                    y1 - cy) ** 2 - radius ** 2 * dx ** 2

        disc = b ** 2 - 4 * a * c

        if disc < 0:
            return []

        t1 = (-b + sqrt(disc)) / (2 * a)
        t2 = (-b - sqrt(disc)) / (2 * a)

        if disc == 0:
            if min(x1, x2) <= t1 <= max(x1, x2):
                y = ((t1 - x1) * dy) / dx + y1
                return [(t1, y)]
            else:
                return []
        elif disc > 0:
            if min(x1, x2) <= t1 <= max(x1, x2) \
                    and min(x1, x2) <= t2 <= max(x1, x2):
                y = ((t1 - x1) * dy) / dx + y1
                yn = ((t2 - x1) * dy) / dx + y1
                return [(t1, y), (t2, yn)]
            elif min(x1, x2) <= t1 <= max(x1, x2):
                y = ((t1 - x1) * dy) / dx + y1
                return [(t1, y)]
            elif min(x1, x2) <= t2 <= max(x1, x2):
                yn = ((t2 - x1) * dy) / dx + y1
                return [(t2, yn)]
            else:
                return []
    else:
        yt1 = sqrt(radius ** 2 - (x1 - center.x) ** 2) + center.y
        yt2 = -sqrt(radius ** 2 - (x1 - center.x) ** 2) + center.y
        if min(y1, y2) <= yt1 <= max(y1, y2) \
                and min(y1, y2) <= yt2 <= max(y1, y2):
            return [(x1, yt1), (x1, yt2)]
        elif min(y1, y2) <= yt1 <= max(y1, y2):
            return [(x1, yt1)]
        elif min(y1, y2) <= yt2 <= max(y1, y2):
            return [(x1, yt2)]
        return []


def isInside(a, b, c, p):
    A = area2(a, b, c)

    A1 = area2(p, b, c)

    A2 = area2(a, p, c)

    A3 = area2(a, b, p)

    if abs(A) == abs(A1) + abs(A2) + abs(A3):
        return True
    return False


def dist2(a, b):
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)


def area_sect(rad, a):
    return 0.5 * a * rad ** 2


def angle(a, b, p):
    sin1 = (2 * area2(a, b, p)) / (dist2(a, p) * dist2(b, p))
    return sin1


def area_segment(rad, al, a, b, p):
    return area_sect(rad, al) - area2(a, b, p)


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

        # Расстояние до другой точки

    # площадь пересечения треугольника и круга

    @staticmethod
    def area_of_intersection(a, b, c, p, rad):
        # окружность точка или точки треугольника лежат на
        # одной прямой или точки совпадают
        if dist2(a, b) == 0 or dist2(b, c) == 0 or dist2(a, c) == 0 \
                or rad == 0 or area2(a, b, c) == 0:
            return 0
        # 9 случай (треугольник лежит внутри окружности)
        elif dist2(a, p) < rad and dist2(b, p) < rad and dist2(c, p) < rad:
            return abs(area2(a, b, c))
        # 1,2,3, случай (вершины треугольника лежат вне окружности)
        elif dist2(a, p) >= rad and dist2(b, p) >= rad \
                and dist2(c, p) >= rad:
            # стороны треугольника не пересекают окружность
            if len(intersection_segment_circle(a, b, p, rad)) == 0 and len(
                    intersection_segment_circle(a, b, p, rad)) == 0 \
                    and len(intersection_segment_circle(a, b, p, rad)) == 0:
                # окружность лежит внутри треугольника(2)
                if isInside(a, b, c, p):
                    return pi * rad ** 2
                # треугольник лежит вне окружности(1)
                else:
                    return 0
            else:
                l1 = intersection_segment_circle(a, b, p, rad)
                l2 = intersection_segment_circle(a, c, p, rad)
                l3 = intersection_segment_circle(c, b, p, rad)
                # 3 случай
                if len(l1) + len(l2) + len(l3) == 2:
                    l_ob = l1 + l2 + l3
                    p1 = R2Point(l_ob[0][0], l_ob[0][1])
                    p2 = R2Point(l_ob[1][0], l_ob[1][1])
                    al = angle(p1, p2, p)
                    pl = area_segment(asin(al), rad, p1, p2, p)
                    return pl
                # 4 случай
                elif len(l1) + len(l2) + len(l3) == 4:
                    if len(l1) == 0:
                        p1 = R2Point(l3[0][0], l3[0][1])
                        p2 = R2Point(l2[0][0], l2[0][1])
                        p3 = R2Point(l3[1][0], l3[1][1])
                        p4 = R2Point(l2[1][0], l2[1][1])
                        al = angle(p1, min_dist(p1, p2, p4), p)
                        al2 = angle(p3, min_dist(p3, p2, p4), p)
                        s = area_sect(rad, asin(al)) + area2(p1, p3, p) + \
                            area2(p2, p4, p) + area_sect(rad, asin(al2))
                        return s
                    elif len(l2) == 0:
                        p1 = R2Point(l3[0][0], l3[0][1])
                        p2 = R2Point(l1[0][0], l1[0][1])
                        p3 = R2Point(l3[1][0], l3[1][1])
                        p4 = R2Point(l1[1][0], l1[1][1])
                        al = angle(p2, min_dist(p2, p1, p3), p)
                        al2 = angle(p4, min_dist(p4, p3, p1), p)
                        s = area_sect(rad, asin(al)) + area2(p1, p3, p) + \
                            area2(p2, p4, p) + area_sect(rad, asin(al2))
                        return s
                    elif len(l3) == 0:
                        p1 = R2Point(l2[0][0], l2[0][1])
                        p2 = R2Point(l1[0][0], l1[0][1])
                        p3 = R2Point(l2[1][0], l2[1][1])
                        p4 = R2Point(l1[1][0], l1[1][1])
                        al = angle(p2, min_dist(p2, p1, p3), p)
                        al2 = angle(p4, min_dist(p4, p1, p3), p)
                        s = area_sect(rad, asin(al)) + abs(area2(p1, p3, p)) + \
                            abs(area2(p2, p4, p)) + area_sect(rad, asin(al2))
                        return s

                # 5 случай
                elif len(l1) + len(l2) + len(l3) == 6:
                    p1 = R2Point(l1[0][0], l1[0][1])
                    p2 = R2Point(l1[1][0], l1[1][1])
                    p3 = R2Point(l2[0][0], l2[0][1])
                    p4 = R2Point(l2[1][0], l2[1][1])
                    p5 = R2Point(l3[0][0], l3[0][1])
                    p6 = R2Point(l3[1][0], l3[1][1])
                    s = area2(p1, p2, p) + area2(p3, p4, p) + area2(p5, p6, p)
                    al = angle(p1, min_dist(p1, min_dist(p1, p3, p4), min_dist(p1, p5, p6)), p)
                    al2 = angle(p2, min_dist(p2, min_dist(p2, p3, p4), min_dist(p2, p5, p6)), p)
                    p7 = min_dist(c, p4, p3)
                    al3 = angle(p7, min_dist(p7, p5, p6), p)
                    s_ob = s + area_sect(rad, asin(al)) + area_sect(rad, asin(al2)) \
                           + area_sect(rad, al3)
                    return s_ob
        # одна вершина треугольника лежит в окружности (6, 7 случай)
        elif (dist2(a, p) < rad and dist2(b, p) >= rad and dist2(c, p) >= rad) or \
                (dist2(a, p) >= rad and dist2(b, p) < rad and dist2(c, p) >= rad) or \
                (dist2(a, p) >= rad and dist2(b, p) >= rad and dist2(c, p) < rad):
            l1 = intersection_segment_circle(a, b, p, rad)
            l2 = intersection_segment_circle(a, c, p, rad)
            l3 = intersection_segment_circle(c, b, p, rad)
            # 7 случай
            if len(l1) + len(l2) + len(l3) == 2:
                if (dist2(a, p) < rad and dist2(b, p) >= rad and dist2(c, p) >= rad):
                    l_ob = l1 + l2 + l3
                    p1 = R2Point(l_ob[0][0], l_ob[0][1])
                    p2 = R2Point(l_ob[1][0], l_ob[1][1])
                    al = angle(p1, p2, p)
                    return area_segment(rad, asin(al), p1, p2, p) + area2(a, p1, p2)
                if (dist2(a, p) >= rad and dist2(b, p) < rad and dist2(c, p) >= rad):
                    l_ob = l1 + l2 + l3
                    p1 = R2Point(l_ob[0][0], l_ob[0][1])
                    p2 = R2Point(l_ob[1][0], l_ob[1][1])
                    al = angle(p1, p2, p)
                    return area_segment(rad, asin(al), p1, p2, p) + area2(b, p1, p2)
                if (dist2(a, p) >= rad and dist2(b, p) >= rad and dist2(c, p) < rad):
                    l_ob = l1 + l2 + l3
                    p1 = R2Point(l_ob[0][0], l_ob[0][1])
                    p2 = R2Point(l_ob[1][0], l_ob[1][1])
                    al = angle(p1, p2, p)
                    return area_segment(rad, asin(al), p1, p2, p) + area2(c, p1, p2)
            # 6 случай
            elif len(l1) + len(l2) + len(l3) == 4:
                if len(l1) == 2:
                    p1 = R2Point(l1[0][0], l1[0][1])
                    p2 = R2Point(l1[1][0], l1[1][1])
                    p3 = R2Point(l2[0][0], l2[0][1])
                    p4 = R2Point(l3[0][0], l3[0][1])
                    s = area2(p, p1, p2) + area2(p1, min_dist(p1, p3, p4), c) \
                        + area2(p2, min_dist(p2, p3, p4), c)
                    al = angle(p1, min_dist(p1, p3, p4), p)
                    al2 = angle(p2, min_dist(p2, p3, p4), p)
                    return s + area_segment(rad, asin(al), p1, min_dist(p1, p3, p4), p) \
                           + area_segment(rad, asin(al2), p2, min_dist(p2, p3, p4), p)
                elif len(l2) == 2:
                    p1 = R2Point(l2[0][0], l2[0][1])
                    p2 = R2Point(l2[1][0], l2[1][1])
                    p3 = R2Point(l1[0][0], l1[0][1])
                    p4 = R2Point(l3[0][0], l3[0][1])
                    s = area2(p, p1, p2) + area2(p1, min_dist(p1, p3, p4), c) \
                        + area2(p2, min_dist(p2, p3, p4), c)
                    al = angle(p1, min_dist(p1, p3, p4), p)
                    al2 = angle(p2, min_dist(p2, p3, p4), p)
                    return s + area_segment(rad, asin(al), p1, min_dist(p1, p3, p4), p) \
                           + area_segment(rad, asin(al2), p2, min_dist(p2, p3, p4), p)
                elif len(l3) == 2:
                    p1 = R2Point(l3[0][0], l3[0][1])
                    p2 = R2Point(l3[1][0], l3[1][1])
                    p3 = R2Point(l1[0][0], l1[0][1])
                    p4 = R2Point(l2[0][0], l2[0][1])
                    s = area2(p, p1, p2) + area2(p1, min_dist(p1, p3, p4), c) \
                        + area2(p2, min_dist(p2, p3, p4), c)
                    al = angle(p1, min_dist(p1, p3, p4), p)
                    al2 = angle(p2, min_dist(p2, p3, p4), p)
                    return s + area_segment(rad, asin(al), p1, min_dist(p1, p3, p4), p) \
                           + area_segment(rad, asin(al2), p2, min_dist(p2, p3, p4), p)



        # 8 случай (две вершины треугольника лежат внутри окружности)
        elif (dist2(a, p) <= rad and dist2(b, p) <= rad and dist2(c, p) > rad) or \
                (dist2(a, p) <= rad and dist2(b, p) > rad and dist2(c, p) <= rad) or \
                (dist2(a, p) <= rad and dist2(b, p) <= rad and dist2(c, p) > rad):
            l1 = intersection_segment_circle(a, b, p, rad)
            l2 = intersection_segment_circle(a, c, p, rad)
            l3 = intersection_segment_circle(c, b, p, rad)
            l_ob = l1 + l2 + l3
            p1 = R2Point(l_ob[0][0], l_ob[0][1])
            p2 = R2Point(l_ob[1][0], l_ob[1][1])
            al = angle(p1, p2, p)
            s_sect = area_segment(rad, asin(al), p1, p2, p)
            if dist2(a, p) <= rad and dist2(b, p) <= rad and dist2(c, p) > rad:
                s = area2(a, b, c) - area2(p1, p2, c) + s_sect
                return s
            elif dist2(a, p) <= rad and dist2(b, p) > rad and dist2(c, p) <= rad:
                s = area2(a, b, c) - area2(p1, p2, b) + s_sect
                return s
            else:
                s = area2(a, b, c) - area2(p1, p2, a) + s_sect
                return s

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False


if __name__ == "__main__":  # pragma: no cover
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
