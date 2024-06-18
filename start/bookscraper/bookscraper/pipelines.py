# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import sqlite3


class BookscraperPipeline:
    def process_item(self, item, spider):
        #nettoyer le prix
        item = self.clean_price(item)
        item = self.clean_stock_lvl2(item)
    
        #nettoyer autre chose
        #nettoyer autre chose
        #nettoyer autre chose
        return item
    
    def clean_price(self,item):
        adapter = ItemAdapter(item)
        price = adapter.get('price')
        cleaned_price = price.replace('£', '')
        adapter['price'] = float(cleaned_price)
        return item
    
    # def clean_stock_lvl1(self,item):
    #     adapter = ItemAdapter(item)
    #     stock = adapter.get('stock')
    #     adapter['stock'] = stock.strip()
    #     return item
    
    def clean_stock_lvl2(self,item):
        adapter = ItemAdapter(item)
        stock = adapter.get('stock')
        adapter['stock'] = int(re.search(r'([0-9]+)', stock).group(0))
        return item
    
class DatabasePipeline:

    def open_spider(self, spider):
        # Se connecter à la base de données
        # Créer une table si elle n'existe pas déjà
        self.connection = sqlite3.connect('books.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                stock INTEGER,
                upc TEXT,
                price REAL
            )
        ''')
        self.connection.commit()

    def process_item(self, item, spider): 
        # Insérer des données dans une BDD
        self.cursor.execute('''
            INSERT INTO books(
                title,
                stock,
                upc,
                price) 
                VALUES (?,?,?,?)''', 
                (item['title'],     
                item['stock'],
                item['upc'], 
                item['price'])
                )
        self.connection.commit()
        return item

    def close_spider(self, spider):
        # Fermer la connexion avec la BDD
        self.connection.close()