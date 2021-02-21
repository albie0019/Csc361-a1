#!/usr/bin/python3

from socket import *
import ssl
import argparse


def GetCode(data):
    # Try to get the status code and return as number
    lines = data.split("\r\n")
    MessageHeader = lines[0]
    MessageWords = MessageHeader.split(" ")
    #print(MessageWords)    #debug
    for word in MessageWords:
        if word.isdigit():
            return int(word)
    
    return -1  # In case no message was recieved or status code not found


def GetCookies(data):
    #Use re to Get Cookies
    cookie_list = []
    lines = data.split("\r\n") # Seperate whole data into lines

    for line in lines:
        if "Set-Cookie:" in line: # Cookie found, store it in list
            cookie_list.append(line)

    return cookie_list


def HTTP11Call(Website):
    # Code to call HTTP 1.1
    print("\n\n*** Starting HTTP 1.1 Connection ***")

    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection.
    s.connect((Website, 80))            # Bind and Connect
    #request_str = "GET " + Website + "/ HTTP/1.1\r\nConnection: keep-alive\r\n\r\n"
    request_str = "GET / HTTP/1.1\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    print("\n" + request_str)
    sending = request_str.encode()
    s.send(sending) # Sending request
    print("***Request Send***\n")
    data = s.recv(10000)
    print("*** Response recieved ***\n" + data.decode() + "\n\n End of response\n")  # Printing the recieved data
    s.close()
    StatusCode = GetCode(data.decode())     # Get the http status code from data message

    cookie_list = GetCookies(data.decode(errors = 'ignore'))

    if(StatusCode in range(300, 399) or StatusCode == 200):
        return (True, cookie_list)
    else:
        return (False, cookie_list)
    


def HTTPSCall(Website):
    # Code to call HTTPS (HTTP1.1 over ssl)
    print("\n\n*** Starting HTTPS Connection ***")

    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection
    contextobj = ssl.wrap_socket(s)         # The socket is now wrapped with contextobj
    contextobj.connect((Website, 443))  # Bind and Connect

    request_str = "GET / HTTP/1.1\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    print( "\n" + request_str)
    sending = request_str.encode()
    contextobj.send(sending)            # Sending request
    data = contextobj.recv(10000)
    print("*** Data recieved ***\n" + data.decode())               # Printing the recieved data
    contextobj.close()

    cookie_list = GetCookies(data.decode(errors = 'ignore'))

    StatusCode = GetCode(data.decode())
    if(StatusCode in range(300, 399) or StatusCode == 200):
        return (True, cookie_list)
    else:
        return (False, cookie_list)


def HTTP2Call(Website):
    # Code to call HTTP2
    print("\n\n*** Starting HTTP2 Connection ***")

    def_context = ssl.create_default_context()
    def_context.set_alpn_protocols(['h2', 'http/1.1'])
    
    s = socket(AF_INET, SOCK_STREAM)    # Starting to build socket connection
    s.connect((Website, 443))           # Bind and Connect
    contextsocketobj = def_context.wrap_socket(s, server_hostname= Website)     # The socket is now wrapped with contextsocketobj

    request_str = "GET / HTTP/1.1\r\nHost:" + Website + "\r\nConnection: keep-alive\r\n\r\n"
    print(request_str)
    sending = request_str.encode()
    contextsocketobj.send(sending)            # Sending request
    #data = contextsocketobj.recv(10000)

    result = False
    if contextsocketobj.selected_alpn_protocol() == 'h2':
        print("Selected ALPN Protocol: H2\n")
        result = True
    else:
        print("Selected ALPN Protocol: Not H2\n")
        result = False
    contextsocketobj.close()

    if(result):
        return True
    else:
        return False
    

def main():

    parser = argparse.ArgumentParser()                                               
    parser.add_argument("website", help="Add the website you wish to contact. Format (www.<website name>.<domain>)") 
    args = parser.parse_args()   
    Website = args.website     # Website name parsed from the command line

    print("\n** Intermediate Output (Optional)**\n")
    (DoesH11Connect, c_list1) = HTTP11Call(Website)
    (DoesHSConnect, c_list2) = HTTPSCall(Website)
    DoesHTTP2Connect = HTTP2Call(Website)

    cookie_list = c_list2 if DoesHSConnect else c_list1
    Cookiestr = ""
    for cookie in cookie_list:
        crumble = cookie.split(";")
        Cookiestr += "\n\nCookie-Name:" + crumble[0].split(":")[1].split("=")[0]
        for c in crumble:
            if "expires" in c:
                Cookiestr += "\nExpiry:" + c.split("=")[1]
            if "Expires" in c:
                Cookiestr += "\nExpiry:" + c.split("=")[1]
            if "domain" in c:
                Cookiestr += "\nDomain:" + c.split("=")[1] 
            if "Domain" in c:
                Cookiestr += "\nDomain:" + c.split("=")[1] 

    #Print the results
    print("**Mandatory Output**")
    print("1. Does the website support HTTPS: " + ("Yes" if DoesHSConnect else "No"))
    print("2. Does the website support HTTP1.1: " + ("Yes" if DoesH11Connect else "No"))
    print("3. Does the website support HTTP2: " + ("Yes" if DoesHTTP2Connect else "No"))
    print("4. Cookies Recieved: " + Cookiestr + "\n")


if __name__ == "__main__":
    main()