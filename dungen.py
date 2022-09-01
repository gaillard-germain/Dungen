from random import randint, choice


class Dungen:
    CHARS = {
        'start': 's',
        'end': 'e',
        'corridor': ' ',
        'room': chr(183),
        'wall': chr(9619),
        'door': '/',
        'void': chr(9608)
        }

    def __init__(self, tile_number=200):
        self.map = {}
        self.tile_number = tile_number
        self.frame = [0, 0, 0, 0]

    def get_nexts(self, coord, gap, diag=False):
        x, y = coord

        if diag:
            for n in range(-gap, gap*2, gap):
                for m in range(-gap, gap*2, gap):
                    if m or n:
                        coord = (x + m, y + n)
                        if coord not in self.map:
                            yield(coord)
        else:
            for i in (-gap, gap):
                coord_x = (x+i, y)
                coord_y = (x, y+i)

                if coord_x not in self.map:
                    yield (x+i, y)

                if coord_y not in self.map:
                    yield (x, y+i)

    def check_nexts(self, coord, gap):
        for tile in self.get_nexts(coord, gap):
            if len(list(self.get_nexts(tile, 1, True))) == 8:
                yield tile

    def tile(self, coord, name):
        if coord not in self.map:
            self.map[coord] = name
            self.tile_number -= 1

    def sign(self, nbr):
        if not nbr:
            return nbr
        else:
            return int(nbr / abs(nbr))

    def get_path(self, start, end):
        x, y = end[0] - start[0], end[1] - start[1]
        vector = (self.sign(x), self.sign(y))
        path = [start]

        while path[-1][0] != end[0]:
            path.append((path[-1][0] + vector[0], path[-1][1]))

        while path[-1][1] != end[1]:
            path.append((path[-1][0], path[-1][1] + vector[1]))

        return path

    def build(self, coord, name, gap):
        neighbors = list(self.check_nexts(coord, gap))

        if neighbors:
            next = choice(neighbors)
            for i, path in enumerate(self.get_path(coord, next)):
                self.tile(path, name)

            if name == 'room':
                for tile in self.get_nexts(next, 1, True):
                    self.tile(tile, name)

            return next

    def fork(self, iter, coord):
        name = self.map[coord]
        for i in range(iter):
            if name == 'room':
                gap = 3
            else:
                gap = 2

            if randint(1, 100) < 60 or i == iter-1:
                name = 'room'
                gap = 3
            else:
                name = 'corridor'

            coord = self.build(coord, name, gap)

            if not coord:
                return

    def door_up(self):
        pass

    def brick_up(self):
        for tile in self.map.copy().keys():
            for coord in self.get_nexts(tile, 1, True):
                self.map[coord] = 'wall'

    def frame_up(self):
        x = [x[0] for x in self.map.keys()]
        y = [y[1] for y in self.map.keys()]
        self.frame[0] = min(x)
        self.frame[1] = max(x)
        self.frame[2] = min(y)
        self.frame[3] = max(y)

    def gen(self):
        coord = (0, 0)
        self.tile(coord, 'start')

        while self.tile_number > 0:
            self.fork(randint(5, 10), coord)
            coord = choice(list(self.map.keys()))

        self.door_up()
        self.brick_up()
        self.frame_up()

    def display(self):
        for y in range(self.frame[2]-1, self.frame[3]+2, 1):
            line = ''
            for x in range(self.frame[0]-1, self.frame[1]+2, 1):
                if (x, y) in self.map:
                    line += self.CHARS[self.map[(x, y)]] * 2
                else:
                    line += self.CHARS['void'] * 2

            print(line)

        print("\nNumber of tiles: {}\n".format(
            len([x for x in self.map.values() if x != 'wall'])))


if __name__ == "__main__":
    dungen = Dungen(300)
    dungen.gen()
    dungen.display()
