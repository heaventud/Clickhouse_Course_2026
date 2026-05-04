#!/usr/bin/env python3

import sys


def total_price(quantity: float, price: float) -> float:
    return quantity * price


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        quantity_str, price_str = line.split("\t")
        result = total_price(float(quantity_str), float(price_str))
        print(result)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
