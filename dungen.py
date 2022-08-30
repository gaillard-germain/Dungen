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
        self.void = 'X'

    def get_neighbors(self, point, diag=False, gap=2):
        """ Return a list of coords adjacent to a point (x, y) using range """

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

    def update_minmax(self, coord):
        if coord[0] < self.min_x:
            self.min_x = coord[0]
        elif coord[0] > self.max_x:
            self.max_x = coord[0]
        if coord[1] < self.min_y:
            self.min_y = coord[1]
        elif coord[1] > self.max_y:
            self.max_y = coord[1]

    def create_corridor(self, coord, room=False):
        neighbors = list(self.get_neighbors(coord))
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

    def create_room(self):
        pass

    def dig(self, iter, current):
        current = current
        for i in range(iter):
            room = False
            if randint(1, 100) < 5:
                room = True
            if randint(1, 100) < 10:
                self.branches.append(current)
                self.dig(randint(5, 10), current)
            if i == iter-1:
                current = self.create_corridor(current, True)
            else:
                current = self.create_corridor(current, room)
            if not current:
                if self.branches:
                    current = self.branches.pop()
                else:
                    break

    def gen(self):
        current = (0, 0)
        self.map[current] = self.floor
        self.dig(self.iter, current)

    def display(self):
        for y in range(self.min_y-1, self.max_y+2, 1):
            line = ''
            for x in range(self.min_x-1, self.max_x+2, 1):
                if (x, y) in self.map:
                    line += '{}'.format(self.map[(x, y)])
                else:
                    line += '{}'.format(self.void)
            print(line)


if __name__ == "__main__":
    dungen = Dungen(50)
    dungen.gen()
    dungen.display()
