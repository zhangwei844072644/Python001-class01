# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from cat.items import CatItem


class MovieSpider(scrapy.Spider):
    name = 'catmovie'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3&offset=0']#有start_requests方法不需要此行

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3&sortId=3'
        cookies = {'BIDUPSID':'066E55BBC5719A8C242AA98AB25777E3',
         'PSTM':'1590070177',
        #   'BAIDUID'=066E55BBC5719A8C6571FD3D8F766277:FG=1,
          'HMACCOUNT':'37B5592EF13A5C9E',
           'BDSFRCVID':'bzPsJeCCxG3_-ljuNdz4XByYBfmuxgp93R2i3J',
           'H_BDCLCKID_SF':'tRk8oIL2fIvMqRjnMPoKq4u_KxrXb-uXKKOLVboLLPOkeqOJ2Mt5BIujMlowKnIJygr8hloDa45WePtwDpKKMjtpexbH55uDJnI83J',
            'BDORZ':'B490B5EBF6F3CD402E515D22BCDA1598',
             'delPer':'0',
             'PSINO':'7',
              'H_PS_PSSID':'1421_32125_21102_32140_31762_32045_31709_32110',
         'HMVT':'6bcd52f51e9b3dce32bec4a3997715ac|1593100631|'}
        yield scrapy.Request(url=url, callback=self.parse,cookies=cookies, dont_filter=False)
    

    def parse(self, response):
        print('(--------------------------)')
        print(response.url)
        movies = Selector(response=response).xpath('//dd')
        
        for i, movie in enumerate(movies):
            item = CatItem()
            if i > 9:
                break
            movie_name = movie.xpath('.//span[@class="name "]/text()')
            movie_type = movie.xpath('.//div[@class="movie-hover-title"]/text()').getall()[4].strip()
            movie_time = movie.xpath('.//div[@class="movie-hover-title movie-hover-brief"]/text()').getall()[1].strip()
            print('--------------------------------')
            print(movie)
            print('+++++++++++++++++++++++++++++++++++')
            print(movie_name.get())
            item['movie_name'] = movie_name.get()
            print(movie_type)
            item['movie_type'] = movie_type
            print(movie_time)
            item['movie_time'] = movie_time
            item['movie_number'] = str(i+1)
            yield item

