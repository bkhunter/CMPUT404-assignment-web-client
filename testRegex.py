
import re

url1 = 'www.localhost.com/'
url2 = 'https://www.google.ca/klklklklhttp://'
url3 = 'http://127.0.0.1:8080/index/'
url4 = 'http://www.google.ca/index/https://'
url5 = 'www.nba.com/spurs/http//'

urls = [url1,url2,url3,url4,url5]

def getHost(url):
    result = re.sub('(https://)|(http://)','',url,1)
    host = re.split('/',result)
    return host[0]

def getPort(host):
    result = re.split(':', host)
    print result[1]

def getPath(url,host):
    path = re.split(host,url)
    return path[1]

h = getHost(url3)
getPort(h)

for url in urls:
    host = getHost(url)
    print 'host= ' + host
    path = getPath(url,host)
    print 'path= ' + path
    print '--------------'
