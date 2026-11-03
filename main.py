"""Demo script that uses the calculator module."""

from calculator import Calculator


def main():
    x, y = 10, 4
    calculator = Calculator()

    print(f"{x} + {y} = {calculator.add(x, y)}")
    print(f"{x} - {y} = {calculator.subtract(x, y)}")
    print(f"{x} * {y} = {calculator.multiply(x, y)}")


if __name__ == "__main__":
    main()
