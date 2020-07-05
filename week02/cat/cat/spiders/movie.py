# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from cat.items import CatItem


class MovieSpider(scrapy.Spider):
    name = 'catmovie'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']#有start_requests方法不需要此行

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        cookies = {'BIDUPSID':'066E55BBC5719A8C242AA98AB25777E3',
         'PSTM':'1590070177',
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
        movies = Selector(response=response).xpath('//dd')
        
        for i, movie in enumerate(movies):
            item = CatItem()
            if i > 9:
                break
            movie_name = movie.xpath('./div[2]/@title').get().strip()
            movie_type = movie.xpath('.//div[1]/text()[2]').get().strip()
            movie_time = movie.xpath('.//div[@class="movie-hover-title movie-hover-brief"]/text()').getall()[1].strip()
            item['movie_name'] = movie_name
            item['movie_type'] = movie_type
            item['movie_time'] = movie_time
            item['movie_number'] = str(i+1)
            yield item

