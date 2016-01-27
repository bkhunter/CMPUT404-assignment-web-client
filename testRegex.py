
import re

url1 = 'www.localhost.com/'
url2 = 'https://www.google.ca/klklklklhttp://'
url3 = 'http://127.0.0.1:8080/index/'
url4 = 'http://www.google.ca/index/https://'
url5 = 'www.nba.com/spurs/http//'

urls = [url1,url2,url3,url4,url5]

sampleResponse = """HTTP/1.0 403 Forbidden
Content-Length: 1103
Content-Type: text/html; charset=UTF-8
Date: Wed, 27 Jan 2016 19:13:26 GMT
Server: GFE/2.0

<html><head><meta http-equiv="content-type" content="text/html; charset=utf-8"/><title>Sorry...</title><style> body { font-family: verdana, arial, sans-serif; background-color: #fff; color: #000; }</style></head><body><div><table><tr><td><b><font face=sans-serif size=10><font color=#4285f4>G</font><font color=#ea4335>o</font><font color=#fbbc05>o</font><font color=#4285f4>g</font><font color=#34a853>l</font><font color=#ea4335>e</font></font></b></td><td style="text-align: left; vertical-align: bottom; padding-bottom: 15px; width: 50%"><div style="border-bottom: 1px solid #dfdfdf;">Sorry...</div></td></tr></table></div><div style="margin-left: 4em;"><h1>Were sorry...</h1><p>... but your computer or network may be sending automated queries. To protect our users, we cant process your request right now.</p></div><div style="margin-left: 4em;">See <a href="https://support.google.com/websearch/answer/86640">Google Help</a> for more information.<br/><br/></div><div style="text-align: center; border-top: 1px solid #dfdfdf;"><a href="https://www.google.com">Google Home</a></div></body></html>"""

class testUrlParse:
    def getHost(self,url):
        result = re.sub('(https://)|(http://)','',url,1)
        host = re.split('/',result)
        return host[0]

    def getPort(self,host):
        result = re.split(':', host)
        print result[1]

    def getPath(self,url,host):
        path = re.split(host,url)
        return path[1]

def test1():
    t= testUrlParse()
    h = t.getHost(url3)
    t.getPort(h)

    for url in urls:
        host = t.getHost(url)
        print 'host= ' + host
        path = t.getPath(url,host)
        print 'path= ' + path
        print '--------------'

def test2():
    response = re.split('\n', sampleResponse)
    
    header = ''
    body = ''
    i = 0
    while (i < len(response)):
        if response[i] == '':           # found separator
           body += response[i+1]
           break
        else:
           header += response[i]+'\r\n'
        i += 1

    print "header:\n"
    print header
    print "body:\n"
    print body

if __name__ == '__main__':
    #test1()
    test2()
    

 

