from random import randint, choice
from viewer import Viewer


class Dungen:
    def __init__(self):
        self.tiles = {}
        self.room_num = 0

    def get_neighbors(self, point, gap, diag=False):
        x, y = point

        if diag:
            for i in range(-gap, gap*2, gap):
                for j in range(-gap, gap*2, gap):
                    yield (x + j, y + i)
        else:
            for i in range(-gap, gap*2, gap):
                yield (x+i, y)
                if i:
                    yield (x, y+i)

    def get_tilables(self, point, gap, diag=False):
        for point in self.get_neighbors(point, gap, diag):
            if point not in self.tiles:
                yield point

    def get_tiles(self, name, excluded=False):
        for k, v in self.tiles.items():
            if excluded:
                if v != name:
                    yield k
            else:
                if v == name:
                    yield k

    def tile_up(self, point, name):
        self.tiles[point] = name

    def brick_up(self):
        for i in list(self.get_tiles('wall', True)):
            for j in self.get_tilables(i, 1, True):
                self.tiles[j] = 'wall'

    def create_room(self, point):
        iter = randint(1, 6)

        for i in range(iter):
            for j in self.get_tilables(point, 1, True):
                if j == point:
                    self.tile_up(j, 'center')
                else:
                    self.tile_up(j, 'floor')

            nexts = list(self.get_tilables(point, 3))

            if nexts and i != iter - 1:
                point = choice(nexts)
            else:
                break

        self.brick_up()
        self.room_num -= 1

    def sign(self, nbr):
        if not nbr:
            return nbr
        else:
            return int(nbr / abs(nbr))

    def get_path(self, point1, point2):
        x, y = point2[0] - point1[0], point2[1] - point1[1]
        vector = (self.sign(x), self.sign(y))
        path = [point1]

        while path[-1][0] != point2[0]:
            path.append((path[-1][0] + vector[0], path[-1][1]))

        while path[-1][1] != point2[1]:
            path.append((path[-1][0], path[-1][1] + vector[1]))

        path.remove(point1)
        path.remove(point2)

        return path

    def create_corridor(self, point1, point2):
        path = self.get_path(point1, point2)

        for i, j in enumerate(path):
            if j in self.get_tiles('wall'):
                self.tiles[j] = 'door'
            elif i == int((len(path)-1) / 2) and i != 1:
                self.tiles[j] = 'center'
            else:
                self.tiles[j] = 'floor'

    def gen(self, room_num):
        self.tiles.clear()
        self.room_num = room_num
        point1 = None

        while self.room_num:
            if not point1:
                self.create_room((0, 0))

            nexts = None
            while not nexts:
                point1 = choice(list(self.get_tiles('center')))
                nexts = list(self.get_tilables(point1, 4))

            point2 = choice(nexts)
            self.create_room(point2)

            self.create_corridor(point1, point2)

        return self.tiles


if __name__ == "__main__":
    viewer = Viewer()
    dungeon = Dungen().gen(10)
    viewer.display(dungeon)
