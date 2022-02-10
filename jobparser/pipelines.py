# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies0302

    def process_item(self, item, spider):
        # salary = self.process_salary(item.get('salary'))
        # item['salary_min'], item['salary_max'], item['cur'] = salary
        # del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    @staticmethod
    def process_salary(dirty_salary):
        min_salary, max_salary, cur = 0, 0, 'руб'
        # .....
        return min_salary, max_salary, cur