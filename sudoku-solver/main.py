import gui
from grid import Grid
from solver import solve


def main():
    with open('data/30-numbers.txt') as f:
        data = f.readline().strip()
        grid = Grid.from_data(data)
        print('Solving')
        print(grid)

        solution = solve(grid)
        print()
        print('Found solution')
        print(solution)


if __name__ == '__main__':
    main()
