import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

#电影网址
url = 'https://maoyan.com/films?showType=3'
#浏览器头

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'Cookie': '__mta=19265031.1593047889495.1593060720154.1593072589344.4; uuid_n_v=v1; uuid=BA7C34C0B68111EAA2F937AFDFBC83F658D0CACF\
            0DAB427597B4733CE126B46D; _csrf=d71f89d46a52b57a8c21d53d596df6d66199d2619e1e0b1774a8ce8942b85386; _lxsdk_cuid=172e90db60ac8-0b2ae\
            5e7cded07-4353761-144000-172e90db60ac8; _lxsdk=BA7C34C0B68111EAA2F937AFDFBC83F658D0CACF0DAB427597B4733CE126B46D; mojo-uuid=7b486d\
            607322ff4fb1728356f2071938; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593047889,1593072687; mojo-session-id={"id":"38fedb863751288\
            326ba172a250cb0a4","time":1593076762367}; mojo-trace-id=1; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593076762; __mta=19265031.159\
            3047889495.1593072589344.1593076762589.5; _lxsdk_s=172eac647b2-046-6c-c1c%7C%7C3'
}

#请求
rs = requests.get(url, headers=header)
print(rs.status_code)
print(rs.text)
#解析
bs_info = bs(rs.text,'xml')

#找到电影块
movie_list = []
for i, movie in enumerate(bs_info.find_all('dd') ) :
    if i > 9:
        break
    name = movie.find('span', class_='name ').text#取出电影名
    tags = movie.find_all('div',class_='movie-hover-title')
    movie_type = tags[1].contents[2].strip()#取出电影上映时间
    movie_time = movie.find('div', class_='movie-hover-title movie-hover-brief').contents[2].strip()#取出电影上映时间
    movie_list.append(f'编号{i+1}')
    movie_list.append('电影名：'+name)
    movie_list.append('类型：'+movie_type)
    movie_list.append('上映时间：'+movie_time)
    movie_list.append('')
print(movie_list)
#保存
movie1 = pd.DataFrame(data = movie_list)
movie1.to_csv('./catmovie1.csv', encoding='utf8', index=False, header=False)
    




