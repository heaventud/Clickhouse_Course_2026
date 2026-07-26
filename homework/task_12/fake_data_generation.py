import argparse
import sys

import faker


TABLE_NAME = "default.user_activity"
DEFAULT_ROWS = 10_000
DEFAULT_USERS = 1_000
ACTIVITY_TYPES = [
    "login",
    "logout",
    "page_view",
    "search",
    "add_to_cart",
    "purchase",
    "refund",
    "support_request",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate raw INSERT query for default.user_activity."
    )
    parser.add_argument("--rows", type=int, default=DEFAULT_ROWS)
    parser.add_argument("--users", type=int, default=DEFAULT_USERS)
    return parser.parse_args()


def quote_string(value: str):
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def generate_user_ids(fake: faker.Faker, users_count: int):
    return [
        fake.random_int(min=1, max=2**32 - 1)
        for _ in range(users_count)
    ]


def generate_row(fake: faker.Faker, user_ids: list[int]):
    user_id = fake.random_element(elements=user_ids)
    activity_type = fake.random_element(elements=ACTIVITY_TYPES)
    activity_date = fake.date_time_between(
        start_date="-1y",
        end_date="now",
    ).strftime("%Y-%m-%d %H:%M:%S")

    return (
        f"({user_id}, "
        f"{quote_string(activity_type)}, "
        f"{quote_string(activity_date)})"
    )


def main() -> int:
    args = parse_args()
    fake = faker.Faker()
    user_ids = generate_user_ids(fake, args.users)

    print(f"INSERT INTO {TABLE_NAME} (user_id, activity_type, activity_date) VALUES")
    for row_number in range(args.rows):
        separator = "," if row_number < args.rows - 1 else ";"
        print(generate_row(fake, user_ids) + separator)
    return 0


if __name__ == "__main__":
    sys.exit(main())
