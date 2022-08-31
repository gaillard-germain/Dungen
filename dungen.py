from random import randint, choice


class Dungen:
    CHARS = {
        'floor': ' ',
        'wall': '#',
        'void': '.'
    }

    def __init__(self, tile_number):
        self.map = {}
        self.tile_number = tile_number
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0

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

    def update_minmax(self, coord):
        if coord[0] < self.min_x:
            self.min_x = coord[0]
        elif coord[0] > self.max_x:
            self.max_x = coord[0]

        if coord[1] < self.min_y:
            self.min_y = coord[1]
        elif coord[1] > self.max_y:
            self.max_y = coord[1]

    def tile(self, coord):
        self.map[coord] = self.CHARS['floor']
        self.tile_number -= 1

    def build(self, coord, room=False):
        neighbors = list(self.check_nexts(coord))

        if neighbors:
            next = choice(neighbors)
            self.tile(next)

            if room:
                room = self.get_nexts(next, True, 1)
                for tile in room:
                    self.tile(tile)
                    self.update_minmax(tile)
            else:
                self.update_minmax(next)
                path = (int((coord[0] + next[0]) / 2),
                        int((coord[1] + next[1]) / 2))
                self.tile(path)

            return next

    def fork(self, iter, current):
        for i in range(iter):
            room = False

            if randint(1, 100) < 10 or i == iter-1:
                room = True

            current = self.build(current, room)

            if not current or self.tile_number < 0:
                return

    def brick_up(self):
        for tile in self.map.copy().keys():
            for coord in self.get_nexts(tile, True, 1):
                self.map[coord] = self.CHARS['wall']

    def gen(self):
        current = (0, 0)
        self.tile(current)

        while self.tile_number > 0:
            current = self.fork(randint(5, 10), current)

            if not current:
                current = choice(list(self.map.keys()))

        self.brick_up()

    def display(self):
        for y in range(self.min_y-1, self.max_y+2, 1):
            line = ''
            for x in range(self.min_x-1, self.max_x+2, 1):
                if (x, y) in self.map:
                    line += self.map[(x, y)]
                else:
                    line += self.CHARS['void']

            print(line)

        print("\nNumber of tile: {}\n".format(
            len([x for x in self.map.values() if x == ' '])))


if __name__ == "__main__":
    dungen = Dungen(200)
    dungen.gen()
    dungen.display()
