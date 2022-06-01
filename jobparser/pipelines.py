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
        self.mongobase = client.vacancies0902

    def process_item(self, item, spider):
        salary = self.process_salary(item.get('salary'), spider)
        item['salary_min'], item['salary_max'], item['cur'] = salary
        del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    @staticmethod
    def process_salary(dirty_salary, spider):
        min_salary, max_salary, cur = None, None, None
        if spider.name == 'hhru':
            for index, value in enumerate(dirty_salary):
                if value.strip() == 'от':
                    min_salary = int(dirty_salary[index + 1].replace('\xa0', ''))
                if value.strip() == 'до':
                    max_salary = int(dirty_salary[index + 1].replace('\xa0', ''))
            if len(dirty_salary) > 1:
                cur = dirty_salary[-2]
        if spider.name == 'superjobru':
            if 'от' in dirty_salary:
                dirty_salary.remove('\xa0')
                min_salary = int(dirty_salary[1].replace('\xa0', '').replace('руб.', ''))
                cur = 'руб.'
            elif 'до' in dirty_salary:
                dirty_salary.remove('\xa0')
                max_salary = int(dirty_salary[1].replace('\xa0', '').replace('руб.', ''))
                cur = 'руб.'
            elif '—' in dirty_salary:
                for item in dirty_salary:
                    if item == '\xa0':
                        dirty_salary.remove('\xa0')
                min_salary = int(dirty_salary[0].replace('\xa0', ''))
                max_salary = int(dirty_salary[2].replace('\xa0', ''))
                cur = dirty_salary[-1]

        return min_salary, max_salary, cur
