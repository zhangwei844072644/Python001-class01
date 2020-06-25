# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd

class CatPipeline:
    def process_item(self, item, spider):
        movie_name = item['movie_name']
        movie_type = item['movie_type']
        movie_time = item['movie_time']
        movie_number = item['movie_number']
        output = f'|{movie_number}|\t|{movie_name}|\t|{movie_type}|\t|{movie_time}|\n\n'
        with open('./maoyan.txt', 'a+', encoding='utf-8') as article:
            article.write(output)
            article.close()
        movie_list=[]
        movie_list.append(movie_number)
        movie_list.append(movie_name)
        movie_list.append(movie_type)
        movie_list.append(movie_time)
        movie1 = pd.DataFrame(data = movie_list)
        movie1.to_csv('./maoyan.csv',mode='a', encoding='utf8', index=False, header=False)
        return item
