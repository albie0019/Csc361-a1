#!/usr/bin/python3

from socket import *
from ssl import *
import argparse
import re

def GetCookies(data):
    #Use re to Get Cookies
    print("b")

def HTTP10Call(Website):
    # Code to call HTTP 1.0
    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection.
    s.connect((Website, 80)) # Connect
    #request_str = "GET " + Website + "/ HTTP/1.1\r\nConnection: keep-alive\r\n\r\n"
    request_str = "GET / HTTP/1.1\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    sending = request_str.encode()
    s.send(sending) # Sending request
    data = s.recv(100000)
    print(data.decode())  # Printing the recieved data
    s.close()


def HTTP11Call(Website):
    # Code to call HTTP 1.1
    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection.
    s.connect((Website, 80))            # Bind and Connect
    #request_str = "GET " + Website + "/ HTTP/1.1\r\nConnection: keep-alive\r\n\r\n"
    request_str = "GET / HTTP/1.1\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    sending = request_str.encode()
    s.send(sending) # Sending request
    data = s.recv(10000)
    print(data.decode())  # Printing the recieved data
    s.close()
    #print("y")
    return True

def HTTPSCall(Website):
    # Code to call HTTPS (HTTP1.1 over ssl)

    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection
    contextobj = wrap_socket(s)         # The socket is now wrapped with contextobj
    contextobj.connect((Website, 443))  # Bind and Connect

    request_str = "GET / HTTP/1.1\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    sending = request_str.encode()
    contextobj.send(sending) # Sending request
    data = contextobj.recv(10000)
    print(data.decode())  # Printing the recieved data
    contextobj.close()
    return True
    #print("x")

def HTTP2Call():
    # Code to call HTTP2
    print("n")


def main():

    parser = argparse.ArgumentParser()                                               #Change this before you embaress yourself!
    parser.add_argument("website", help="Add the website you wish to contact. Format (www.<website name>.<ending>)") 
    args = parser.parse_args()   
    Website = args.website     # Website name parsed from the command line
    #print(Website)
    DoesH11Connect = HTTP11Call(Website)
    DoesHSConnect = HTTPSCall(Website)

    #Print the results
    print("Mandatory Output")
    print("1. Does the website support HTTP1.1: " + str(DoesH11Connect))
    print("2. Does the website support HTTPS: " + str(DoesHSConnect))

if __name__ == "__main__":
    main()