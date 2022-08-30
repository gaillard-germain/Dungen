from random import randint, choice


class Dungen:
    def __init__(self, iter):
        self.map = {}
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        self.iter = iter
        self.branches = []
        self.floor = ' '
        self.wall = '#'
        self.void = '.'

    def get_neighbors(self, point, diag=False, gap=2):
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

    def check(self, coord):
        for tile in self.get_neighbors(coord):
            if len(list(self.get_neighbors(tile, True, 1))) == 8:
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

    def build(self, coord, room=False):
        neighbors = list(self.check(coord))

        if neighbors:
            next = choice(neighbors)
            self.map[next] = self.floor

            if room:
                room = self.get_neighbors(next, True, 1)
                for tile in room:
                    self.map[tile] = self.floor
                    self.update_minmax(tile)
            else:
                self.update_minmax(next)
                path = (int((coord[0] + next[0]) / 2),
                        int((coord[1] + next[1]) / 2))
                self.map[path] = self.floor

            return next

    def plan(self, iter, current):
        for i in range(iter):
            room = False

            if randint(1, 100) < 10 or i == iter-1:
                room = True

            if randint(1, 100) < 20:
                self.branches.append(current)
                self.plan(randint(3, 15), current)

            current = self.build(current, room)

            if not current:
                if self.branches:
                    current = self.branches.pop()

                else:
                    break

    def brick_up(self):
        for tile in self.map.copy().keys():
            for coord in self.get_neighbors(tile, True, 1):
                self.map[coord] = self.wall

    def gen(self):
        current = (0, 0)
        self.map[current] = self.floor
        self.plan(self.iter, current)
        self.brick_up()

    def display(self):
        for y in range(self.min_y-1, self.max_y+2, 1):
            line = ''
            for x in range(self.min_x-1, self.max_x+2, 1):
                if (x, y) in self.map:
                    line += self.map[(x, y)]
                else:
                    line += self.void

            print(line)


if __name__ == "__main__":
    dungen = Dungen(30)
    dungen.gen()
    dungen.display()
