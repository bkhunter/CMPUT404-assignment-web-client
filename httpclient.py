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
    print "httpclient.py [GET/POST] [URL]\n"

#probably should be called a HTTPResponse
class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    
    def get_host_port(self,url):
        strippedUrl = re.sub('(https://)|(http://)','',url,1)
        splitUrl = re.split('/',strippedUrl)
        host = splitUrl[0]
        if ':' in host:
            splitHost = re.split(':', host)
            host = splitHost[0]
            port = splitHost[1]
        else:
            # port not specified
            port = 80
        return host,port

    def connect(self, host, port):
        #from lab
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host,port))
        return clientSocket
        
        # use sockets!
        #return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

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

    def GET(self, url, args=None):
        host,port = self.get_host_port(url)
        print host
        print
        print port
        port = int(port)
        host = 'www.google.com'
        port = 80
        sock = self.connect(host,port)
        request = "GET / HTTP/1.0\r\n "
        sock.sendall(request)

        print self.recvall(sock)
        
        
        
        code = 200
        body = ""
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url,command="GET",args=None):
        print 'url='+url
        print 'command='+ command

        #call connect
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"

    #input: httpclient.py [GET/POST] [URL]\n

    #input: httpclient.py [URL] [GET/POST]\n
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
