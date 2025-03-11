import fill_database as fd
from faker import Faker

fake = Faker()
Faker.seed(0)

fd.insert_products_rows(fd.generate_products_rows(1000))
fd.insert_seasons_rows(fd.seasons)
fd.insert_stores_rows(fd.generate_stores_rows())
fd.insert_styles_rows(fd.generate_styles_rows())
fd.insert_customers_rows(fd.generate_customers_rows(2500))
fd.insert_occasions_rows(fd.occasions)
