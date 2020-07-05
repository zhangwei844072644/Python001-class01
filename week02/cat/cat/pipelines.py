# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import pymysql

class CatPipeline:
    

    def __init__(self):
        dbInfo = {
                    'host' : 'localhost',
                    'port' : 3306,
                    'user' : 'root',
                    'password' : 'root',
                    'db' : 'test',
                    'table':'猫眼'
                }
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        self.table = dbInfo['table']

    def open_spider(self, spider):
        #开启连接
        self.conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db,
            charset='utf8mb4',
        )
        #创建游标
        self.cur = self.conn.cursor()
    
    def process_item(self, item, spider):
        try:
            #跟同窗学的,用字符串的format方法让代码看起来很清爽
            sql_fmt = ("""INSERT INTO `{}`(`电影`, `类型`, `上映日期`) VALUES ('{}', '{}', '{}');""")
            sql = sql_fmt.format(self.table, item['movie_name'], item['movie_type'],item['movie_time'])
            self.cur.execute(sql)
            self.conn.commit()
            return item	
        except  :
            #保存失败，回滚操作
            self.conn.rollback()

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
    
    def close_spider(self, spider):
        #运行结束关闭连接
        self.conn.close()

