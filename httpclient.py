#!/usr/bin/env python
# coding: utf-8

# Copyright 2013 Abram Hindle
# Copyright 2016 Ben Hunter
#
# See README For detailed licensing information regarding Ben Hunter
# and collaboration
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

# Parameter reversed from skeleton
def help():
    print "httpclient.py [URL] [GET/POST]\n"

# Changed name from skeleton
class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
    def __str__(self):
        codeStr = '\n'+'HTTP Response Code: ' +str(self.code) + '\n'
        return codeStr + self.body

# Class for handling the formation of HTTP requests
class HTTPRequest():
        def __init__(self,host,port):
            self.userLine = "User-Agent: Ben's HTTP Client\r\n"
            if port==80:
                self.hostLine= "Host:"+host+"\r\n"
            else:
                # must specify port if it not 80
                self.hostLine= "Host:"+host+':'+str(port)+"\r\n"
            self.acceptLine= "Accept: */*\r\n"
            self.connectLine = "Connection: closed\r\n"
            self.contentLine = "Content-Type: application/x-www-form-urlencoded\r\n"
            self.req = self.userLine + self.hostLine + self.acceptLine + self.connectLine + self.contentLine

        # form get request
        def makeGet(self,path):
            initLine = "GET "+path+" HTTP/1.1\r\n"
            return initLine + self.req + '\r\n'

        # form Post request
        def makePost(self,path,args):
             initLine = "POST "+path+" HTTP/1.1\r\n"
             if args is None:
                 return initLine + self.req + '\r\n'
             else:
                 body = urllib.urlencode(args)
                 length = len(body)
                 lenLine = "Content-Length: "+str(length)+'\r\n'
                 return initLine + self.req + lenLine + '\r\n' + body


class HTTPClient(object):
    
    # using regular expressions and string manipulation, parses
    # the URL to extract the host, port, and path
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

    # Get the HTTP response code, raises ValueError if error in input
    def get_code(self, data):
        match = re.match(r'.* (\d\d\d) .*',data)
        if match is None:
            raise ValueError('code parsed is not HTTP compliant. Could not parse HTTP code in "%s"' %data)
        else:
            code = match.group(1)
        return int(code)

    # Parses socket data as a string to extract the header, body and code
    def parseResponse(self,data):
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

    # Creates an HTTP GET request for the specified URL, sends the request,
    # and recieves and parses the response.If there are arguments, they are 
    # encoded and appended to the path
    def GET(self, url, args=None):

        #args = {'a' : '☃'}

        # I want to append any arguments to the URL
        if args is None:
            args = ''
        else:
            args = urllib.urlencode(args)
            if '?' in url:
                args = '&'+args
            else:
                args = '?'+args

        # parse the URL for the potential port, and the host and path
        host,port,path = self.get_host_port_path(url)

        path += args            # add arguments
        sock = self.connect(host,port) # make connection
        
        # Form request
        requestObject = HTTPRequest(host,port)
        request = requestObject.makeGet(path)
        
        # Send request
        sock.sendall(request)

        # Parse response
        data = self.recvall(sock)
        header,body,code = self.parseResponse(data)
        return HTTPResponse(code, body)

    # Creates an HTTP POST request for the URL and arguments specified,
    # sends the request, and parses the response
    def POST(self, url, args=None):

        host,port,path = self.get_host_port_path(url) # parse path
        sock = self.connect(host,port)                # make connection
        
        # form request
        request = HTTPRequest(host,port)
        request = request.makePost(path,args)

        # send request
        sock.sendall(request)

        # parse response
        data = self.recvall(sock)
        header,body,code = self.parseResponse(data)
        return HTTPResponse(code, body)

    def command(self, url,command="GET",args=None):
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
