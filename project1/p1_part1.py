from socket import *
import sys
import string
import time

port = 8888
max_connections = 1

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('localhost',port))
tcpSerSock.listen(max_connections)

def recvall(sock):
    BUFF_SIZE = 4096
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

while 1:

    # Start receiving data from the client
    print ('Ready to serve...')
    
    tcpCliSock, addr = tcpSerSock.accept()
    print( 'Received a connection from:', addr)
    
    message = tcpCliSock.recv(1024)
    #print( message)
    
    # Extract the filename from the given message
    print (message.split()[1])
    filename = message.decode().split()[1].partition("//")[0].replace("/","") # partition("//")[i] the number i changes on your use case
    
    try:
        # Check whether the file exist in the cache
        with open(filename, "r") as f:
            outputdata = f.readlines()
        resp = "".join(outputdata)
        tcpCliSock.send(resp.encode())
        
        print ('Read from cache')
    
    # Error handling for file not found in cache
    except IOError:
        # Create a socket on the proxyserver
        proxy_socket = socket(AF_INET, SOCK_STREAM)
        hostn = filename
        print ("hostn:",hostn)
        try:
            # Connect to the socket to port 80
            proxy_socket.connect((hostn, 80))
            print('filename', filename)
            
            # Create a temporary file on this socket and ask port 80 for the file requested by the client
            
            header = "GET "+"http://" + filename + " HTTP/1.1\r\n"+ "Host: " + filename +"\r\n\r\n"
            print(header)
            proxy_socket.send(header.encode('utf-8'))

            time.sleep(1) # need to sleep to make sure all data will be there once we try to recieve it
            resp = recvall(proxy_socket)
            response = resp.decode()
            print(response)
            
            # Create a new file in the cache for the requested file.
            # Also send the response in the buffer to client socket and the corresponding file in the cache
            if(filename[-1:] == '/'):
                filename = filename[:-1]

            with open(filename,"wb") as tmpFile:
                tmpFile.write(resp)
                print("saved file as:",filename)
            
            tcpCliSock.send(resp)
        except Exception as e:
            print (str(e))
            print ("Illegal request")

    # Close the client and the server sockets
    tcpCliSock.close()
