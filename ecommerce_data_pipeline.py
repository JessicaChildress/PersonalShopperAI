import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import json
from sqlalchemy import create_engine
from faker import Faker
from datetime import datetime
import logging
import concurrent.futures
import time
from typing import List, Dict, Any

class ClothingDataPipeline:
    def __init__(self, db_connection_string: str):
        self.engine = create_engine(db_connection_string)
        self.fake = Faker()
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('ClothingDataPipeline')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def scrape_h_and_m(self, num_pages: int = 5) -> List[Dict[str, Any]]:
        """Scrape H&M product data"""
        base_url = "https://www2.hm.com/en_us/women/products/view-all.html"
        products = []
        
        for page in range(num_pages):
            try:
                url = f"{base_url}?page={page}"
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                for product in soup.find_all('div', class_='product-item'):
                    products.append({
                        'name': product.find('h3', class_='item-heading').text.strip(),
                        'price': float(product.find('span', class_='price').text.replace('$', '')),
                        'description': product.find('span', class_='description').text.strip(),
                        # Add more fields as needed
                    })
                    
                time.sleep(1)  # Respectful scraping
            except Exception as e:
                self.logger.error(f"Error scraping page {page}: {str(e)}")
                
        return products

    def fetch_shopify_products(self, store_url: str, access_token: str) -> List[Dict[str, Any]]:
        """Fetch products from a Shopify store API"""
        headers = {'X-Shopify-Access-Token': access_token}
        products = []
        
        try:
            response = requests.get(f"{store_url}/admin/api/2024-01/products.json", headers=headers)
            data = response.json()
            products.extend(data['products'])
        except Exception as e:
            self.logger.error(f"Error fetching Shopify products: {str(e)}")
            
        return products

    def generate_synthetic_data(self, num_records: int = 1000) -> Dict[str, pd.DataFrame]:
        """Generate synthetic data for testing and development"""
        # Generate products
        products = []
        for i in range(num_records):
            products.append({
                'product_id': i,
                'name': f"{self.fake.color()} {self.fake.word()} {['Dress', 'Shirt', 'Pants', 'Jacket'][i % 4]}",
                'brand_id': np.random.randint(1, 21),
                'base_price': round(np.random.uniform(20, 200), 2),
                'current_price': round(np.random.uniform(15, 180), 2),
                'description': self.fake.text(max_nb_chars=200),
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
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

    def process_and_clean_data(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Clean and standardize raw data"""
        df = pd.DataFrame(data)
        
        # Basic cleaning
        df = df.dropna(subset=['name', 'price'])
        df['name'] = df['name'].str.strip()
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        # Add derived features
        df['price_category'] = pd.qcut(df['price'], q=4, labels=['budget', 'moderate', 'premium', 'luxury'])
        
        return df

    def run_pipeline(self, sources: List[str] = ['synthetic', 'h_and_m', 'shopify']) -> None:
        """Run the complete data pipeline"""
        all_data = {}
        
        if 'synthetic' in sources:
            synthetic_data = self.generate_synthetic_data()
            all_data.update(synthetic_data)
            
        if 'h_and_m' in sources:
            h_and_m_data = self.scrape_h_and_m()
            cleaned_h_and_m = self.process_and_clean_data(h_and_m_data)
            all_data['h_and_m_products'] = cleaned_h_and_m
            
        if 'shopify' in sources:
            # Add Shopify credentials here
            shopify_data = self.fetch_shopify_products("STORE_URL", "ACCESS_TOKEN")
            cleaned_shopify = self.process_and_clean_data(shopify_data)
            all_data['shopify_products'] = cleaned_shopify
            
        self.load_to_database(all_data)

if __name__ == "__main__":
    # Usage example
    pipeline = ClothingDataPipeline('postgresql://username:password@localhost:5432/clothing_db')
    pipeline.run_pipeline(['synthetic'])  # Start with synthetic data