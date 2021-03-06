import random
from collections import namedtuple
from math import sqrt
from typing import Iterable

import numpy as np
from PIL import Image

Point = namedtuple('Point', ('coords', 'n', 'center'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))


def get_points(img: Image):
    width, height = img.size
    return [
        Point(color, 3, count)
        for (count, color) in img.getcolors(width*height)
    ]

def flatten_rgb(rgb):
    return [x for x in rgb]


def euclidean(p1: Point, p2: Point):
    return sqrt(sum((
        (p1.coords[i] - p2.coords[i]) ** 2
        for i in range(p1.n)
    )))


def calculate_center(points: Iterable[Point], n: int):
    plen = sum(map(lambda point: point.center, points))
    vals = [sum(p.coords[i]*p.center for p in points ) for i in range(n)]

    return Point([(v / plen) for v in vals], n, 1)


def kmeans(points: Iterable[Point], k: int, min_diff: float):
    clusters = [Cluster([point], point, point.n) for point in random.sample(points, k)]

    while True:
        plists = [[] for _ in range(k)]

        for point in points:
            smallest_distance = float('Inf')
            for i, cluster in enumerate(clusters):
                distance = euclidean(point, cluster.center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    id = i
            plists[id].append(point)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters


def get_dominant_colour(pixels: np.ndarray):
    img = Image.fromarray(pixels)
    img.thumbnail((200, 200))
    points = get_points(img)
    clusters = kmeans(points, 5, 7)
    rgbs = (map(int, c.center.coords) for c in clusters)
    rgbs = [flatten_rgb(rgb) for rgb in rgbs]
    contrasts = []
    for i, [r, g, b] in enumerate(rgbs):
        contrasts.append(min(
            abs(r - g),
            abs(r - b),
            abs(b - g),
        ))
    # print(contrasts)
    [r, g, b] = rgbs[np.argmax(contrasts)]
    if r == max(r, g, b):
        return 'R'
    elif g == max(r, g, b):
        return 'G'
    else:
        return 'B'


def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1, a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]
