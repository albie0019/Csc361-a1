from socket import *
s = socket(AF_INET, SOCK_STREAM)
s.connect(("www.uvic.ca", 80)) # Connect
sending = "GET uvic.ca/index.html HTTP/1.1\n\n".encode()
s.send(sending) # Sending request
data = s.recv(10000)
print(data.decode())
s.close()

