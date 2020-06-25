import urllib.request

def getHtml(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html = response.read()
    return html

def saveHtml(file_name,file_content):
    with open(file_name.replace('/','_')+'.html','wb') as f:
        f.write(file_content)


html = getHtml("https://maoyan.com/films?showType=3&offset=0")
saveHtml("test",html)
print("结束")