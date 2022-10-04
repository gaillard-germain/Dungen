from dungen import Dungen
from viewer import Viewer


class Console:
    def __init__(self):
        self.dungen = Dungen()
        self.viewer = Viewer()
        self.choice = ["Building", "Cave"]

    def run(self):
        while True:
            print("\n{}\n".format("DUNGEN".center(20, "#")))
            print("A random dungeon generator\n")
            print("Define the number of rooms.")

            nbr = input("Number of rooms: ")

            print("Choose a type.")

            for i, j in enumerate(self.choice):
                print("\t{}.{}".format(i, j))

            type = input("Type: ")

            self.viewer.display(self.dungen.gen(int(nbr), int(type)))

            print("Generation time: {} seconds\n".format(
                round(self.dungen.time, 3)))

            com = input("Do you want to generate another dungeon? (y/n): ")

            if com == 'n':
                break


if __name__ == "__main__":
    Console().run()
