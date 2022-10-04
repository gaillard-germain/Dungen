#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

from math import cos, sin, radians


__all__ = ["Tools", "get_neighbors_range", "get_neighbors_math"]


class Tools:

    @staticmethod
    def get_neighbors_range(point, gap, diag=False):
        """ Return a list of coords adjacent to a point (x, y) using range """

        x, y = point

        if diag:
            for i in range(-gap, gap*2, gap):
                for j in range(-gap, gap*2, gap):
                    if i or j:
                        yield((x + j, y + i))
        else:
            for i in range(-gap, gap*2, gap):
                if i:
                    yield (x+i, y)
                    yield (x, y+i)

    @staticmethod
    def get_neighbors_math(point, gap, diag=False):
        """ Return a list of coords adjacent to a point (x, y) using math """

        x, y = point
        compass = 0

        while compass < 360:
            yield((x + gap*round(cos(radians(compass))),
                   y + gap*round(sin(radians(compass)))))
            if diag:
                compass += 45
            else:
                compass += 90


if __name__ == '__main__':
    point = (2, 2)
    print(list(Tools.get_neighbors_range(point, 1, True)))
    print(list(Tools.get_neighbors_math(point, 1, True)))


get_neighbors_range = Tools.get_neighbors_range
get_neighbors_math = Tools.get_neighbors_math
