class Viewer:
    CHARS = {
        'floor': ' ',
        'center': ' ',
        'door': '/',
        'wall': chr(9619),
        'void': chr(9608)
        }

    def __init__(self):
        self.tiles = {}
        self.frame = [0, 0, 0, 0]

    def frame_up(self):
        x = [x[0] for x in self.tiles.keys()]
        y = [y[1] for y in self.tiles.keys()]
        self.frame[0] = min(x)
        self.frame[1] = max(x)
        self.frame[2] = min(y)
        self.frame[3] = max(y)

    def display(self, tiles):
        self.tiles = tiles
        self.frame_up()

        for y in range(self.frame[2]-1, self.frame[3]+2, 1):
            line = ''
            for x in range(self.frame[0]-1, self.frame[1]+2, 1):
                if (x, y) in self.tiles:
                    line += self.CHARS[self.tiles[(x, y)]] * 2
                else:
                    line += self.CHARS['void'] * 2

            print(line)

        print("\nNumber of tiles: {}\n".format(
            len([x for x in self.tiles.values() if x != 'wall'])))
