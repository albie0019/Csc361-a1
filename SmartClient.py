#!/usr/bin/python3

from socket import *
import ssl
import argparse
import re


def GetCode(data):
    # Try to get the status code and return as number
    lines = data.split("\r\n")
    MessageHeader = lines[0]
    MessageWords = MessageHeader.split(" ")
    print(MessageWords)
    for word in MessageWords:
        if word.isdigit():
            return int(word)
    
    return -1  # In case no message was recieved or status code not found


def GetCookies(data):
    #Use re to Get Cookies
    """
    cookiepatt = "[^Set\-Cookie](\S.+)" # Pattern string to match cookie
    cookie_list = []              # List to store cookie
    lines = data.split("\r\n")
    #print(lines)

    for line in lines:
        cookie_match = re.match(cookiepatt, line)
        
        if cookie_match:
            cookies = cookie_match.group()
            cookie_list.append(cookies)
    """
    cookie_list = []
    lines = data.split("\r\n")

    for line in lines:
        if "Set-Cookie:" in line:
            cookie_list.append(line)

    return cookie_list


def HTTP10Call(Website):
    # Code to call HTTP 1.0
    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection.
    s.connect((Website, 80)) # Connect
    #request_str = "GET " + Website + "/ HTTP/1.1\r\nConnection: keep-alive\r\n\r\n"
    request_str = "GET / HTTP/1.0\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    sending = request_str.encode()
    s.send(sending) # Sending request
    data = s.recv(10000)
    print(data.decode())  # Printing the recieved data
    s.close()


def HTTP11Call(Website):
    # Code to call HTTP 1.1
    print("** Starting HTTP 1.1 Connection **")

    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection.
    s.connect((Website, 80))            # Bind and Connect
    #request_str = "GET " + Website + "/ HTTP/1.1\r\nConnection: keep-alive\r\n\r\n"
    request_str = "GET / HTTP/1.1\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    print(request_str + "\n")
    sending = request_str.encode()
    s.send(sending) # Sending request
    print("**Request Send**")
    data = s.recv(10000)
    print("** Data recieved **" + data.decode())  # Printing the recieved data
    s.close()
    StatusCode = GetCode(data.decode())     # Get the http status code from data message

    if(StatusCode in range(300, 399) or StatusCode == 200):
        return True
    else:
        return False
    


def HTTPSCall(Website):
    # Code to call HTTPS (HTTP1.1 over ssl)
    print("** Starting HTTPS Connection **")

    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection
    contextobj = ssl.wrap_socket(s)         # The socket is now wrapped with contextobj
    contextobj.connect((Website, 443))  # Bind and Connect

    request_str = "GET / HTTP/1.1\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    print(request_str + "\n")
    sending = request_str.encode()
    contextobj.send(sending)            # Sending request
    data = contextobj.recv(10000)
    print("** Data recieved **" + data.decode())               # Printing the recieved data
    contextobj.close()

    cookie_list = GetCookies(data.decode())
    for cookie in cookie_list:
        crumble = cookie.split(";")
        print("\nCookie-Name:" + crumble[0].split(":")[1])
        for c in crumble:
            if "expires" in c:
                print("Expiry:" + c.split("=")[1])
            if "domain" in c:
                print("Domain:" + c.split("=")[1])

    StatusCode = GetCode(data.decode())
    if(StatusCode in range(300, 399) or StatusCode == 200):
        return True
    else:
        return False


def HTTP2Call(Website):
    # Code to call HTTP2
    print("** Starting HTTP2 Connection **")

    """
    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection.
    s.connect((Website, 80))            # Bind and Connect
    #request_str = "GET " + Website + "/ HTTP/1.1\r\nConnection: keep-alive\r\n\r\n"
    request_str = "GET / HTTP/1.1\r\nHost:" + Website + "\r\nConnection: Upgrade, HTTP2-Settings\r\nUpgrade: h2c\r\nConnection: keep-alive\r\n\r\n"
    print(request_str + "\n")
    sending = request_str.encode()
    s.send(sending) # Sending request
    print("**Request Send**")
    data = s.recv(10000)
    print("** Data recieved **" + data.decode())  # Printing the recieved data
    s.close()
    StatusCode = GetCode(data.decode())     # Get the http status code from data message

    if(StatusCode in range(300, 399) or StatusCode == 200):
        return True
    else:
        return False
    """
    #context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context = ssl.create_default_context()
    context.set_alpn_protocols(['h2', 'http/1.1'])
    
    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection
    s.connect((Website, 443))  # Bind and Connect
    contextsocketobj = context.wrap_socket(s, server_hostname= Website)     # The socket is now wrapped with contextobj

    request_str = "GET / HTTP/1.1\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    print(request_str + "\n")
    sending = request_str.encode()
    contextsocketobj.send(sending)            # Sending request
    data = contextsocketobj.recv(10000)
    #print("** Data recieved **" + data.decode())               # Printing the recieved data
    print(contextsocketobj.selected_alpn_protocol())
    result = True
    contextsocketobj.close()
    '''
    cookie_list = GetCookies(data.decode())
    for c in cookie_list:
        print(c)
    
    StatusCode = GetCode(data.decode())
    if((StatusCode in range(300, 399) or StatusCode == 200) and result):
        return True
    else:
        return False
    '''

def main():

    parser = argparse.ArgumentParser()                                               
    parser.add_argument("website", help="Add the website you wish to contact. Format (www.<website name>.<domain>)") 
    args = parser.parse_args()   
    Website = args.website     # Website name parsed from the command line
    #print(Website)
    print("\n** Intermediate Output**\n")
    #DoesH11Connect = HTTP11Call(Website)
    DoesHSConnect = HTTPSCall(Website)
    #DoesHTTP2Connect = HTTP2Call(Website)

    #Print the results
    print("**Mandatory Output**")
    #print("1. Does the website support HTTP1.1: " + str(DoesH11Connect))
    print("2. Does the website support HTTPS: " + str(DoesHSConnect))
    #print("3. Does the website support HTTP2: " + str(DoesHTTP2Connect))
    print("4. Cookies Recieved: ")


if __name__ == "__main__":
    main()