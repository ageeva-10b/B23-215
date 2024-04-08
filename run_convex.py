#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void,Figure

f = Void()
Figure.cen=R2Point()
Figure.rad=float(input("r -> "))
try:

    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}, S_per = {f.area_of_intersection()}\n")
        print(Figure.rad)
except (EOFError, KeyboardInterrupt):
    print("\nStop")

