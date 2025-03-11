# import psycopg2
from connect import load_config, connect
from faker import Faker
import random

config = load_config()
conn = connect(config)

fake = Faker()
Faker.seed(0)


def generate_products_rows(num_records: int = 1000) -> list[tuple]: 
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


def insert_seasons_rows(seasons: list[tuple]):
    with conn.cursor() as cur:
        args_bytes = b','.join(cur.mogrify("(%s, %s, %s, %s, %s)", row) for row in seasons)
        cur.execute(b'INSERT INTO "Seasons" VALUES ' + args_bytes)

    # commit the changes to the database
    conn.commit()
    print('data successfully added to the Seasons table')


def generate_stores_rows() -> list[tuple]:
    stores = []

    for i in range(10):
        stores.append((
            i+10000,
            ['Urban Loom', 'Luxe Haven', 'TrendSavvy', 'Velvet Ember', 
            'The Chic Loft', 'AquaVibe Boutique', 'ModernFlare', 'Ember & Ivy', 
            'Stellar Threads', 'The Twisted Rack'][i % 10],
            ['New York', 'Los Angeles', 'Miami'][i % 3],
            ['https://www.urbanloom.com','https://www.luxehaven.com','https://www.trendsavvy.com',
            'https://www.velvetember.com','https://www.thechicloft.com','https://www.aquavibeboutique.com',
            'https://www.modernflare.com','https://www.emberandivy.com','https://www.stellarthreads.com',
            'https://www.twistedrack.com'][i % 10],
            random.randint(1, 25)
        ))
    return stores

def insert_stores_rows(stores: list[tuple]): 
    with conn.cursor() as cur:
        args_bytes = b','.join(cur.mogrify("(%s, %s, %s, %s, %s)", row) for row in stores)
        cur.execute(b'INSERT INTO "Stores" VALUES ' + args_bytes)

    # commit the changes to the database
    conn.commit()
    print('data successfully added to the Stores table')


def generate_styles_rows() -> list[tuple]:
    styles = []

    for i in range(10):
        styles.append((
            i+1,
            ['Casual', 'Streetwear', 'Bohemian', 'Preppy', 'Chic',
             'Athleisure', 'Gothic', 'Minimalist', 'Vintage', 'Rock/Grunge'][i % 10],
            ["Relaxed and comfortable clothing such as t-shirts, jeans, leggings, sneakers, and hoodies, ideal for everyday wear.",
            "Urban-inspired fashion featuring oversized clothing, graphic t-shirts, sneakers, and accessories, drawing influence from skateboarding and hip-hop cultures.",
            "A free-spirited, relaxed style with flowy dresses, fringed jackets, ethnic prints, and earthy tones, focusing on natural fabrics and laid-back vibes.",
            "Classic American style characterized by polo shirts, blazers, chinos, cardigans, and loafers, often polished and neat.",
            "Sophisticated and stylish, featuring tailored outfits, minimalist elegance, high heels, and high-end accessories for a refined look.",
            "Sporty yet fashionable clothing designed for both exercise and casual wear, such as leggings, joggers, tank tops, and sneakers, blending comfort and style.",
            "Dark, edgy clothing often in black, with leather jackets, boots, fishnets, and heavy accessories, inspired by gothic subcultures and a mysterious aesthetic.",
            "Simple, clean lines and neutral colors with a focus on timeless, functional wardrobe essentials and understated elegance.",
            "Fashion inspired by past decades, from retro dresses to high-waisted pants, featuring pieces that reflect the styles of the 1920s to the 1980s.",
            "Influenced by rock music and the '90s grunge scene, featuring band t-shirts, leather jackets, ripped jeans, boots, and a rebellious, edgy vibe."][i % 10]
        ))
    return styles

def insert_styles_rows(styles: list[tuple]):
    with conn.cursor() as cur:
        args_bytes = b','.join(cur.mogrify("(%s, %s, %s)", row) for row in styles)
        cur.execute(b'INSERT INTO "Styles" VALUES ' + args_bytes)

    # commit the changes to the database
    conn.commit()
    print('data successfully added to the Styles table')


def generate_customers_rows(num_records = 1000) -> list[tuple]:
    customers = []

    for i in range(num_records):
        if i % 3 == 0:
            gender = 'male'
            name = fake.name_male()
        else:
            gender = 'female'
            name = fake.name_female()
        customers.append((
            i+1000,
            name, 
            random.randint(15, 65),
            gender
        ))
    return customers

def insert_customers_rows(customers: list[tuple]):
    with conn.cursor() as cur:
        args_bytes = b','.join(cur.mogrify("(%s, %s, %s, %s)", row) for row in customers)
        cur.execute(b'INSERT INTO "Customers" VALUES ' + args_bytes)

    # commit the changes to the database
    conn.commit()
    print('data successfully added to the Customers table')



def insert_occasions_rows(occasions: list[tuple]):
    with conn.cursor() as cur:
        args_bytes = b','.join(cur.mogrify("(%s, %s, %s)", row) for row in occasions)
        cur.execute(b'INSERT INTO "Occasions" VALUES ' + args_bytes)

    # commit the changes to the database
    conn.commit()
    print('data successfully added to the Occasions table')


occasions = [
    (1, 'Conference', 'Professional events where business attire is common, like suits, dresses, or smart shirts and trousers.'),
    (2, 'Wedding', 'Formal events where guests often wear dresses or suits. Brides and grooms usually wear formal or semi-formal attire.'),
    (3, 'Club', 'Casual to semi-casual outfits, typically trendy or fashionable. Many wear clubbing dresses, trendy tops, jeans, or stylish shoes.'),
    (4, 'Interview', 'Business or business-casual attire, like a suit, dress shirt, or blouse, paired with dress shoes.'),
    (5, 'Casual Day Out', 'Comfortable clothing such as jeans, t-shirts, casual dresses, or comfortable shoes for a relaxed outing.'),
    (6, 'Beach Party', 'Swimwear like bikinis or board shorts, along with cover-ups, flip-flops, or sandals.'),
    (7, 'Formal Gala', 'Elegant, formal dresses or tuxedos, often with accessories like heels, jewelry, and tuxedo shirts or bowties.'),
    (8, 'Concert', 'Casual or trendy clothing depending on the genre of music, such as band t-shirts, denim, or casual dresses.'),
    (9, 'Family Gathering', 'Casual clothing, such as relaxed dresses or jeans with a nice top, suitable for spending time with family.'),
    (10, 'Graduation', 'Academic gowns or formal attire like dresses, skirts, or suits for this celebratory occasion.'),
    (11, 'First Date', 'Smart casual clothing, like nice jeans or skirts, paired with a stylish top or shirt to make a good impression.'),
    (12, 'Holiday Party', 'Festive attire, such as dresses, skirts, or festive sweaters for Christmas, New Year, or other celebrations.'),
    (13, 'Sports Event', 'Team jerseys, athletic wear, or casual clothing suitable for cheering on a team, paired with comfortable shoes.'),
    (14, 'Job Fair', 'Business-casual or professional attire such as dress shirts, blouses, slacks, or skirts to create a good impression.'),
    (15, 'Funeral', 'Formal, respectful attire like dark-colored dresses, suits, or slacks, with conservative accessories.'),
    (16, 'Barbecue', 'Casual, comfortable clothing such as shorts, t-shirts, casual dresses, and flip-flops or sneakers.'),
    (17, 'Art Exhibit', 'Smart-casual clothing, often with a touch of creativity, like fashionable yet comfortable pieces or elegant outfits.'),
    (18, 'Theater', 'Elegant yet comfortable attire like dresses or slacks, often paired with stylish shoes or heels for an evening out.'),
    (19, 'Brunch', 'Casual-chic clothing like a nice blouse, skirts, or dresses, paired with comfortable but fashionable shoes.'),
    (20, 'Camping', 'Outdoor clothing like hiking boots, jackets, cargo pants, and comfortable activewear suitable for nature activities.')
]


seasons = [
    (1, 'Spring', '03-20-2025', '06,20,2025', 'Spring fashion celebrates renewal with lighter fabrics and brighter colors. Floral prints, pastels, and airy dresses are in vogue, along with trench coats and lightweight cardigans. It is a time for more vibrant and playful styles, with comfy sneakers and sandals making their appearance.'),
    (2, 'Summer', '06-21-2025', '09-19-2025', 'Summer fashion focuses on staying cool while looking fresh. Expect light and breathable fabrics such as cotton and linen, paired with shorts, tank tops, sundresses, and swimsuits. Bold colors, tropical prints, and casual footwear like flip-flops and slides are essentials for the warmer months.'),
    (3, 'Fall', '09-20-2025', '12-20-2025', 'Fall fashion is all about layering. Trendy items include cozy knit sweaters, leather jackets, and scarves. Earthy tones like browns, oranges, and deep greens dominate, alongside plaid patterns and boots for both style and comfort.'),
    (4, 'Winter', '12-21-2025', '03-19-2025', 'Winter fashion revolves around staying warm while maintaining style. Key pieces include oversized coats, puffer jackets, turtlenecks, wool sweaters, and chunky scarves. Darker hues like black, navy, and charcoal are popular, with metallic accents and cozy textures like faux fur becoming prominent.')
]


if __name__ == '__main__':
    insert_products_rows(generate_products_rows(fake, 1000))
    insert_seasons_rows(seasons)
    insert_stores_rows(generate_stores_rows(fake))
    insert_styles_rows(generate_styles_rows(fake))
    insert_customers_rows(generate_customers_rows(fake, 2500))
    insert_occasions_rows(occasions)
