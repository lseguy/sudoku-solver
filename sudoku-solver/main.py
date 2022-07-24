import gui
from grid import Grid


def main():
    with open('data/45-numbers.txt') as f:
        data = f.readline().strip()
        grid = Grid.from_data(data)
        print(grid)


if __name__ == '__main__':
    main()
