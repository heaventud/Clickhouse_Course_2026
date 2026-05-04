#!/usr/bin/env python3

import sys


def transaction_category(price: float, baseline: float = 100.0):
    if price > baseline:
        return 'High Value'
    else:
        return 'Low Value'


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        total_price = line.strip()
        result = transaction_category(float(total_price), 1000.0)
        print(result)


if __name__ == "__main__":
    main()
