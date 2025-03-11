# import psycopg2
from connect import load_config, connect
from faker import Faker
import random

config = load_config()
conn = connect(config)

fake = Faker()
Faker.seed(0)

def generate_products_rows(fake: Faker, num_records: int = 1000) -> list[tuple]: 
    products = []
    
    for i in range(num_records):
        base_price = round(random.uniform(10, 150), 2)
        products.append(
            (i,
            ['T-shirt', 'Hoodie', 'Sweater', 'Skirt', 'Pants', 'Shorts', 'Coat', 
            'Jacket', 'Blazer', 'Cardigan', 'Jeans', 'Dress', 'Polo shirt', 'Tank top', 
            'Vest', 'Leggings', 'Jumpsuit', 'Pajamas', 'Romper', 'Overalls', 'Scarf', 
            'Gloves', 'Boots', 'Sneakers', 'Sandals', 'Belt', 'Tie', 'Socks', 'Shirt', 
            'Blouse', 'Suit jacket'][i % 31],
            fake.safe_color_name(),
            ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL'][i % 7],
            [round(x * 0.1, 1) for x in range(10, 51)][i % 41],
            base_price,
            round(base_price * (random.randint(0, 60) / 100), 2))
        )

    return products


def insert_products_rows(products: list[tuple]):
    with conn.cursor() as cur:
        # execute the INSERT statement
        # source: https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
        args_bytes = b','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s, %s)", row) for row in products)
        cur.execute(b'INSERT INTO "Products" VALUES ' + args_bytes)
    
    # commit the changes to the database
    conn.commit()
    
    print('data successfully added to the Products table')

# insert the rows returned by the generator function into the database
insert_products_rows(generate_products_rows(fake, 1000))