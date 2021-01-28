#!/usr/bin/python3

from socket import *
import argparse

def HTTP10Call(Website):
    # Code to call HTTP 1.0
    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection.
    s.connect((Website, 80)) # Connect
    #request_str = "GET " + Website + "/ HTTP/1.1\r\nConnection: keep-alive\r\n\r\n"
    request_str = "GET / HTTP/1.0\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    sending = request_str.encode()
    s.send(sending) # Sending request
    data = s.recv(100000)
    print(data.decode())  # Printing the recieved data
    s.close()


def HTTP11Call():
    # Code to call HTTP 1.1
    print("y")


def HTTPSCall():
    # Code to call HTTPS (HTTP over ssl)
    print("x")

def HTTP2Call():
    # Code to call HTTP2
    print("n")


def main():

    parser = argparse.ArgumentParser()                                               #Change this before you embaress yourself!
    parser.add_argument("website", help="Add the website you wish to contact. Format (www.<website name>.<ending>)") 
    args = parser.parse_args()   
    Website = args.website     # Website name parsed from the command line
    #print(Website)
    HTTP10Call(Website)



if __name__ == "__main__":
    main()