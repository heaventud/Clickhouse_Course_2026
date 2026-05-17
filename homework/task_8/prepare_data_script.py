import random
import faker


fake = faker.Faker()
table_filename = 'table_data.txt'
dict_filename = 'dict_data.csv'
USERS_NUMBER = 1000

ACTIONS = [
    'purchase',
    'refund',
    'subscription',
    'chargeback',
    'bonus',
]


def prepare_dict_source():
    user_list = []
    with open(dict_filename, 'w') as f:
        for i in range(USERS_NUMBER):
            user_id = fake.random_number(digits=8)
            user_email = fake.email()
            user_list.append(user_id)
            f.write(f'{user_id},{user_email}\n')
    return user_list


def prepare_table_source(users: list[int]):
    tbl = []
    for _ in range(10_000):
        user_id = random.choice(users)
        action = random.choice(ACTIONS)
        expense = fake.random_number(digits=3)
        timestamp = fake.date_time_between(end_date='-6m').timestamp()
        tbl.append((user_id, action, expense, timestamp))

    with open(table_filename, 'w') as f:
        f.write('\n'.join(map(str, tbl)))


def main():
    users = prepare_dict_source()
    prepare_table_source(users)


if __name__ == "__main__":
    main()
