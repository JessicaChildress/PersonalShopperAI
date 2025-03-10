import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import json
import psycopg2
from sqlalchemy import create_engine 
from faker import Faker
from datetime import datetime
import logging
import random
import concurrent.futures
import time
from typing import List, Dict, Any

from config import load_config


class FakeClothingDataPipeline():
    def __init__(self, config):
        self.engine = self._connect(load_config())
        self.fake = Faker()
        Faker.seed(0)
        self.logger = self._setup_logger()

    def _connect(self, config):
        """ Connect to the PostgreSQL database server """
        try:
            # connecting to the PostgreSQL server
            with psycopg2.connect(**config) as conn:
                print('Connected to the PostgreSQL server.')
                return conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
    
    def _setup_logger(self):
        """ Creates a data logger """
        logger = logging.getLogger('ClothingDataPipeline')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def generate_synthetic_data(self, num_records: int = 1000) -> Dict[str, pd.DataFrame]:
        """Generate synthetic data for testing and development
        * num_records(int): specifies the number of rows of synthetic data to develop. The default is 1000
        """
        # Generate products
        products = []
        # creates in row in the products table 
        # 
        for i in range(num_records):
            base_price = round(random.uniform(10, 150), 2)
            discounted_price = base_price * (random.randint(0, 75) / 100)
            products.append({
                'ProductId': i,
                'ProductName': {['T-shirt', 'Hoodie', 'Sweater', 'Skirt', 'Pants', 'Shorts', 'Coat', 
                                    'Jacket', 'Blazer', 'Cardigan', 'Jeans', 'Dress', 'Polo shirt', 'Tank top', 
                                    'Vest', 'Leggings', 'Jumpsuit', 'Pajamas', 'Romper', 'Overalls', 'Scarf', 
                                    'Gloves', 'Boots', 'Sneakers', 'Sandals', 'Belt', 'Tie', 'Socks', 'Shirt', 
                                    'Blouse', 'Suit jacket'][i % 31]},
                'ProductColor': self.fake.safe_color_name(),
                'ProductSize': {['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL'][i % 7]},
                'ProductRating': {[round(x * 0.1, 1) for x in range(10, 51)][i % 41]},
                'BasePrice': base_price,
                'DiscountedPrice': discounted_price,
                'active': True
            })

        # Generate product attributes
        attributes = []
        for product_id in range(num_records):
            for attr in ['color', 'material', 'pattern', 'season']:
                attributes.append({
                    'product_id': product_id,
                    'attribute_key': attr,
                    'attribute_value': self.fake.word()
                })

        return {
            'products': pd.DataFrame(products),
            'product_attributes': pd.DataFrame(attributes)
        }
    
    def load_to_database(self, dataframes: Dict[str, pd.DataFrame]) -> None:
        """Load DataFrames to database tables"""
        for table_name, df in dataframes.items():
            try:
                df.to_sql(table_name, self.engine, if_exists='append', index=False)
                self.logger.info(f"Successfully loaded {len(df)} records to {table_name}")
            except Exception as e:
                self.logger.error(f"Error loading data to {table_name}: {str(e)}")