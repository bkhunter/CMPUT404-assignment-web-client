#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [URL] [GET/POST]\n"

#probably should be called a HTTPResponse
class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPRequest():
        def __init__(self,host):
            self.userLine = "User-Agent: Ben's HTTP Client\r\n"
            self.hostLine= "Host:"+host+"\r\n"
            self.acceptLine= "Accept: */*\r\n"
            self.connectLine = "Connection: closed\r\n"
            self.contentLine = "Content-Type: application/x-www-form-urlencoded\r\n"

        def makeGet(self,path):
            initLine = "GET "+path+" HTTP/1.1\r\n"
            get = initLine + self.userLine + self.hostLine + self.acceptLine + self.connectLine + self.contentLine + '\r\n'
            return get

        def makePost(self,path,args):
             initLine = "POST "+path+" HTTP/1.1\r\n"
             data = urllib.urlencode(args)
             length = len(data)
             lenLine = "Content-Length: "+str(length)+'\r\n'
             argLine = data + '\r\n'
             post = initLine + self.userLine + self.hostLine + self.acceptLine + self.connectLine + self.contentLine + lenLine +'\r\n' + argLine
             return post
            
        

class HTTPClient(object):
    
    def get_host_port_path(self,url):
        strippedUrl = re.sub('(https://)|(http://)','',url,1)
        splitUrl = re.split('/',strippedUrl)
        host = splitUrl[0]
        splitPath = re.split(host,url)
        path = splitPath[1]
        if ':' in host:
            splitHost = re.split(':', host)
            host = splitHost[0]
            port = int(splitHost[1])
        else:
            # port not specified
            port = 80
        return host,port,path

    def connect(self, host, port):
        #from lab
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host,port))
        return clientSocket

    def get_code(self, data):
        match = re.match(r'.* (\d\d\d) .*',data)
        if match is None:
            raise ValueError('code parsed is not HTTP compliant. Could not parse HTTP code in "%s"' %data)
        else:
            code = match.group(1)
        return int(code)

    def get_headers(self,data):
        response = data.splitlines()
        splitLine = len(response)
        for i, line in enumerate(response):
            if line == '':
                splitLine = i
                break
        code = self.get_code(response[0])
        body = response[splitLine:]
        header = response[:splitLine]

        body = '\n'.join(body)
        header = '\n'.join(header)
        
        return header,body,code

    def getArgs(self,url):
        match = re.match(r'.*[?](.*)',url)
        if match is None:
            return None
        else:
            return match.group(1)
        

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    # def makeGetRequest(self,path,host):
    #     initLine = "GET "+path+" HTTP/1.1\r\n"
    #     userLine = "User-Agent: Ben's HTTP Client\r\n"
    #     hostLine= "Host:"+host+"\r\n"
    #     acceptLine= "Accept: */*\r\n"
    #     connectLine = "Connection: closed\r\n"
    #     contentLine = "Content-Type: application/x-www-form-urlencoded\r\n"
        
    #     return initLine+userLine+hostLine+acceptLine+connectLine+contentLine + '\r\n'

    def GET(self, url, args=None):
        # example resource /test/demo_form.asp?name1=value1&name2=value2
        host,port,path = self.get_host_port_path(url)
        sock = self.connect(host,port)
        request = HTTPRequest(host)
        request = request.makeGet(path)
        sock.sendall(request)
        data = self.recvall(sock)
        header,body,code = self.get_headers(data)
        print header
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        args =  {'a':'aaaaaaaaaaaaa',
                'b':'bbbbbbbbbbbbbbbbbbbbbb',
                'c':'c',
                'd':'012345\r67890\n2321321\n\r'}

        host,port,path = self.get_host_port_path(url)
        sock = self.connect(host,port)
        request = HTTPRequest(host)
        request = request.makePost(path,args)
        
        print '--------------'
        print request
        code = 500
        body = ""
        return HTTPResponse(code, body)
        # POST /test/demo_form.asp HTTP/1.1
        # Host: w3schools.com
        # name1=value1&name2=value2
        # http://www.w3schools.com/tags/ref_httpmethods.asp

        # POST /~hindle1/1.py HTTP/1.1
        # > User-Agent: curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3
        # > Host: webdocs.cs.ualberta.ca
        # > Accept: */*
        # > Content-Length: 25
        # > Content-Type: application/x-www-form-urlencoded

    def command(self, url,command="GET",args=None):
        print 'url='+url
        print 'command='+ command
        if args is None:
            args = self.getArgs(url)

        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command(sys.argv[1], command)   


# control flow:

# --> command with URL and verb
# -- 
