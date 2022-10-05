#Dylan Dockery
#Server to process HTTP GET requests
#libraries needed : socket, argparse, datetime, os
#instructions: 
#Start via commandline. Commandline parameters are as follows:
#-p --- Port used for server. Required 

from socket import *
from datetime import datetime
import argparse
import os

#logs requests in Common Log Format
def log(addr,request,code, size,userAgent):
    f=open("serverLog.txt","a")
    f.write(addr + ' - - ' + datetime.now().strftime("[%d/%b/%Y:%H:%M:%S %z]") +' '+ request +' '+ code+' ' + size+' ' + userAgent+'\n')
    f.close()

#returns HTTP reponse over connection
def returnMessage(outputdata):
    #sends resource over connection
    for i in range(0, len(outputdata)):
        connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

#determines response to client
def response(requestedResource,HTTPVersion,request,addr,userAgent):
    code200='200'
    code404='404'
    #if no resource requested return index.html
    if requestedResource == '/':
        requestedResource='/index.html'

    #attempts to locate the requested resource if succesful it returns 200 and the resource and if not 404
    try:
        file=open(requestedResource[1:],'r')
        HTTPReponse= HTTPVersion+' 200 OK\r\n'
        outputdata=[HTTPReponse]+file.readlines()
        log(addr, request, code200, str(file.seek(0,os.SEEK_END)),userAgent)
        returnMessage(outputdata)
    except:
        HTTPReponse= HTTPVersion+' 404 Not Found\r\n'
        file=open('error404.html','r')
        outputdata=[HTTPReponse]+file.readlines()
        log(addr, request, code404, str(file.seek(0,os.SEEK_END)),userAgent)
        returnMessage(outputdata)

    
#if an ivalid request is made reurtns 400 error code
def invalidRequest(request,addr,userAgent, HTTPVersion):
    code400='400'
    HTTPReponse= HTTPVersion+' 400 Bad Request\r\n'
    file=open('error400.html','r')
    outputdata=[HTTPReponse]+file.readlines()
    log(addr, request, code400,  str(file.seek(0,os.SEEK_END)),userAgent)
    returnMessage(outputdata)

#command line argmuent declaration
parser = argparse.ArgumentParser(description='Server')
parser.add_argument('-p', type=int, default=8000,help='Port used for server. Required', required=True)
args = parser.parse_args()

#port for the server to use

serverPort=args.p

#indices for parsing the incoming GET request
head=0
HTTPprotocol=0
requestedResource=1
HTTPVersion=2

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))  
print(serverSocket)  
serverSocket.listen(1)
print("The server is ready to receive")
while True:
    
    #opens socket and processes incoming HTTP requests
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024).decode()
    messageSplit=message.split('\r\n')
    requestRaw=messageSplit[0]
    request=requestRaw.split(' ')
    
    #selects the user agent from the HTTP request
    userAgent=''
    for i in messageSplit:
        if i.startswith('User-Agent'):
            userAgent=i.split(' ')[1]

   #processes get requests and returns invalid respnse for none get requests 
    if(request[HTTPprotocol]=='GET'):
        response(request[requestedResource],request[HTTPVersion],requestRaw,addr[0],userAgent)
    else:
        invalidRequest(requestRaw,addr[0],userAgent,request[HTTPVersion])

    connectionSocket.close()