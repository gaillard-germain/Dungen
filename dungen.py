from random import randint, choice, randrange
from viewer import Viewer


class Dungen:
    def __init__(self):
        self.tiles = {}

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
        for i in range(randint(1, 6)):
            for j in self.get_tilables(point, 1, True):
                if j == point:
                    self.tile_up(j, 'center')
                else:
                    self.tile_up(j, 'floor')

            nexts = list(self.get_tilables(point, 3))

            if nexts:
                point = choice(nexts)
            else:
                break

        self.brick_up()

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
            if i == int((len(path)-1) / 2) and i != 1:
                self.tiles[j] = 'center'
            else:
                self.tiles[j] = 'floor'

    def gen(self, room_num, cave=False):
        point = (0, 0)
        while room_num:
            self.create_room(point)
            nexts = None

            while not nexts:
                fork = choice(list(self.get_tiles('center')))
                if cave:
                    corridor_len = randrange(4, 16, 2)
                else:
                    corridor_len = 4
                nexts = list(self.get_tilables(fork, corridor_len))

            point = choice(nexts)
            if room_num > 1:
                self.create_corridor(fork, point)
            room_num -= 1

        return self.tiles


if __name__ == "__main__":
    viewer = Viewer()
    dungeon = Dungen().gen(10, True)
    viewer.display(dungeon)
