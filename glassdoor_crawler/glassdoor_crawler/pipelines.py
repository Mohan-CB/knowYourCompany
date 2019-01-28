# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
import pdb
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GlassdoorCrawlerPipeline(object):
    def process_item(self, item, spider):
        self.storeInDb(item)
        return item

    def __init__(self):
        self.setupDBCon()
        # self.createTables()
    
    def setupDBCon(self):
        try:
            self.conn = sqlite3.connect('../../review.db')
            self.cur = self.conn.cursor()
        except Error as e:
            print(e)
            self.conn.close()
    
    def createTables(self):
        self.dropReviewTable()
        self.createReviewTable()

    def createReviewTable(self):
        self.cur.execute('CREATE TABLE "review" (\
                                                    "Id"	TEXT NOT NULL UNIQUE,\
                                                    "Company"	TEXT NOT NULL,\
                                                    "Title"	TEXT NOT NULL,\
                                                    "StarRating"	INTEGER,\
                                                    "Summary"	TEXT,\
                                                    "Job"	TEXT,\
                                                    "Pros"	TEXT,\
                                                    "Cons"	TEXT\
                                                );')

    def dropReviewTable(self):
        #drop amazon table if it exists
        self.cur.execute("DROP TABLE IF EXISTS Review")

    def storeInDb(self,item):
        insert = "INSERT INTO review (Id, Company, Title, StarRating, Summary, Job, Pros, Cons) VALUES(\"{}\", \"{}\", \"{}\", {}, \"{}\", \"{}\" , \"{}\", \"{}\")"
        insert = insert.format(item.get('uid'),item.get('companyName'), item.get('title'), item.get('starRating'), item.get('summary'), item.get('job'), item.get('pros'), item.get('cons'))
        try:
            self.cur.execute(insert)
            print('------------------------')
            print('Data Stored in Database')
            print('------------------------')
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(e)
