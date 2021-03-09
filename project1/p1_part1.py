from socket import *
import sys
import string

port = 8888
max_connections = 1

# if len(sys.argv) <= 1:
#     print ('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server]')
#     sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('',port))
tcpSerSock.listen(max_connections)

base = True
base_name = ''
while 1:

    # Start receiving data from the client
    print ('Ready to serve...')
    
    tcpCliSock, addr = tcpSerSock.accept()
    print( 'Received a connection from:', addr)
    
    message = tcpCliSock.recv(1024)
    #print( message)
    
    # Extract the filename from the given message
    print (message.split()[1])
    filename = message.decode().split()[1].partition("//")[0].replace("/","")
    
    if base:
        base_name = filename
        base = False
    
    fileExist = "false"
    filetouse = "/" + filename.replace("/","")
    print ('filename',filename)
    print (filetouse)
    
    try:
        # Check whether the file exist in the cache
        with open(filetouse[1:], "r") as f:
            outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(("HTTP/1.1 200 OK\r\n").encode())
        tcpCliSock.send(("Content-Type:text/html\r\n").encode())
        resp = ""
        for s in outputdata:
            resp += s
        
        tcpCliSock.send(resp.encode())
        
        print ('Read from cache')
    
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.split('/')[0].replace("www.","",1) #'.'.join(filename.split('/')[0].replace("www.","",1).split('.')[1:])
            print (hostn)
            try:
                # Connect to the socket to port 80
                c.connect((base_name.split('/')[0], 80))
                print('filename', filename)
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                print("GET "+"http://" + filename + " HTTP/1.1\r\n"+ "Host: " + base_name.split('/')[0] +"\r\n\r\n")
                c.send(("GET "+"http://" + filename + " HTTP/1.1\r\n"+ "Host: " + base_name.split('/')[0] +"\r\n\r\n").encode())
                
                # Show what request was made
                #print ("GET "+"http://" + filename + " HTTP/1.0")

                # Read the response into buffer
                resp = c.recv(4096).decode()
                total = resp.split()[2]
                print(len(resp),"total:",total)
                response = ""
                count = len(resp)
                while resp:
                    response += resp
                    print(response)
                    resp = c.recv(4096).decode()
                    count += len(resp)
                    if count >= total: break
                    print(resp,len(resp))
                print(response)
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                if(filename[-1:] == '/'):
                    filename = filename[:-1]
                print('tempfile part')

                with open(base_name,"wb") as tmpFile:
                    tmpFile.write(response.encode())
                
                tcpCliSock.send(response.encode())
            except Exception as e:
                print (str(e))
                print ("Illegal request")
        else:
            # HTTP response message for file not found
            pass
    
    # Close the client and the server sockets
    tcpCliSock.close()
