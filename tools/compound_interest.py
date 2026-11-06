#!/usr/bin/env python3
"""Calculate compound interest: A = P * (1 + r/n) ** (n * t)."""

import argparse


def compound_interest(principal: float, annual_rate: float, compounds_per_year: int, years: float):
    """Return (final_amount, interest_earned). annual_rate is a percentage, e.g. 7.34."""
    rate = annual_rate / 100
    amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)
    return amount, amount - principal


def non_negative_float(value: str) -> float:
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError(f"must be >= 0, got {value}")
    return number


def positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError(f"must be a positive integer, got {value}")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate compound interest.")
    parser.add_argument("principal", type=non_negative_float, help="initial amount, e.g. 15847")
    parser.add_argument("annual_rate", type=non_negative_float, help="annual interest rate in percent, e.g. 7.34")
    parser.add_argument("compounds_per_year", type=positive_int, help="compounding periods per year, e.g. 12")
    parser.add_argument("years", type=non_negative_float, help="total years, e.g. 8.5833 for 8 years 7 months")
    args = parser.parse_args()

    amount, interest = compound_interest(
        args.principal, args.annual_rate, args.compounds_per_year, args.years
    )
    print(f"Final amount:    {amount:,.2f}")
    print(f"Interest earned: {interest:,.2f}")


if __name__ == "__main__":
    main()
