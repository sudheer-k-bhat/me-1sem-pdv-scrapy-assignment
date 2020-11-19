# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter

class ScrapyArxivOrgPipeline:
    def __init__(self):
      self.create_connection()
      self.create_table()

    def create_connection(self):
      self.conn = sqlite3.connect('papers.db')
      self.curr = self.conn.cursor()
    
    def create_table(self):
      self.curr.execute("""DROP TABLE IF EXISTS tbl_papers""")
      self.curr.execute("""
      CREATE TABLE tbl_papers(
        title text,
        link text,
        abstract text
      )
      """)

    def process_item(self, item, spider):
        self.store_item(item)
        return item

    def store_item(self, item):
      self.curr.execute("""
      INSERT INTO tbl_papers VALUES(?, ?, ?)
      """, (item['title'], item['link'], item['abstract']))
      self.conn.commit()
