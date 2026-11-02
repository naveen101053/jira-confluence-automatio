"""Demo script that uses the calculator module."""

from calculator import add, multiply, subtract


def main():
    x, y = 10, 4

    print(f"{x} + {y} = {add(x, y)}")
    print(f"{x} - {y} = {subtract(x, y)}")
    print(f"{x} * {y} = {multiply(x, y)}")


if __name__ == "__main__":
    main()
