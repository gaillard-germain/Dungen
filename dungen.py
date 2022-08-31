from random import randint, choice


class Dungen:
    CHARS = {
        'floor': ' ',
        'wall': '#',
        'void': '.'
        }

    def __init__(self, tile_number=200):
        self.map = {}
        self.tile_number = tile_number
        self.frame = [0, 0, 0, 0]

    def get_nexts(self, point, diag=False, gap=2):
        x, y = point
        delta = gap

        if diag:
            for n in range(-delta, delta*2, delta):
                for m in range(-delta, delta*2, delta):
                    if m or n:
                        coord = (x + m, y + n)
                        if coord not in self.map:
                            yield(coord)
        else:
            for i in (-delta, delta):
                coord_x = (x+i, y)
                coord_y = (x, y+i)

                if coord_x not in self.map:
                    yield (x+i, y)

                if coord_y not in self.map:
                    yield (x, y+i)

    def check_nexts(self, coord):
        for tile in self.get_nexts(coord):
            if len(list(self.get_nexts(tile, True, 1))) == 8:
                yield tile

    def tile(self, coord):
        self.map[coord] = self.CHARS['floor']
        self.tile_number -= 1

    def build(self, coord, room=False):
        neighbors = list(self.check_nexts(coord))

        if neighbors and self.tile_number > 0:
            next = choice(neighbors)
            self.tile(next)

            if room:
                room = self.get_nexts(next, True, 1)
                if room:
                    for tile in room:
                        if self.tile_number:
                            self.tile(tile)
            else:
                path = (int((coord[0] + next[0]) / 2),
                        int((coord[1] + next[1]) / 2))
                self.tile(path)

            return next

    def fork(self, iter, coord):
        for i in range(iter):
            room = False

            if randint(1, 100) < 10 or i == iter-1:
                room = True

            coord = self.build(coord, room)

            if not coord:
                return

    def brick_up(self):
        for tile in self.map.copy().keys():
            for coord in self.get_nexts(tile, True, 1):
                self.map[coord] = self.CHARS['wall']

    def frame_up(self):
        x = [x[0] for x in self.map.keys()]
        y = [y[1] for y in self.map.keys()]
        self.frame[0] = min(x)
        self.frame[1] = max(x)
        self.frame[2] = min(y)
        self.frame[3] = max(y)

    def gen(self):
        coord = (0, 0)
        self.tile(coord)

        while self.tile_number > 0:
            self.fork(randint(5, 10), coord)
            coord = choice(list(self.map.keys()))

        self.brick_up()
        self.frame_up()

    def display(self):
        for y in range(self.frame[2]-1, self.frame[3]+2, 1):
            line = ''
            for x in range(self.frame[0]-1, self.frame[1]+2, 1):
                if (x, y) in self.map:
                    line += self.map[(x, y)]
                else:
                    line += self.CHARS['void']

            print(line)

        print("\nNumber of tiles: {}\n".format(
            len([x for x in self.map.values() if x == ' '])))


if __name__ == "__main__":
    dungen = Dungen(300)
    dungen.gen()
    dungen.display()
