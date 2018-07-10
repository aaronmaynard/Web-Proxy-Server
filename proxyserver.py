from socket import *
import sys


#port number is arbituary
server_address = ('localhost', 5005)

#create welcoming socket
welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind to the server address
welcomeSocket.bind(server_address)

#begin listening (argument is number of allowed queued connections)
welcomeSocket.listen(1)

#listening loop
while True:
    # Start receiving data from client
    print('WEB PROXY SERVER IS LISTENING')
    
    # Accept() returns a new connection socket along with the address
    clientSocket, clientAddress = welcomeSocket.accept()
    print('WEB PROXY SERVER CONNECTED WITH ' + str(clientAddress))
    print('MESSAGE RECEIVED FROM CLIENT:')
    request = clientSocket.recv(2048)
    print(request)
    
    # Parse Request
    print request.split()[1]
    filename = request.split()[1].partition("/")[2]
    print filename
    fileExist = "false"
    filetouse = "/" + filename
    print filetouse

    # Check if file is already in cache
    try:
        f = open(filetouse[1:0], "r")
        outputdata = f.readlines()
        fileExist = "true"

        # Cache is found
        clientSocket.send("HTTP/1.0 200 OK\r\n")
        clientSocket.send("Content-Type:text/html\r\n")
        for i n range(0, len(outputdata)):
            clientSocket.send(outputdata[i])
        print ('Read from cache")

    # Error handling E404
    except IOError
        if fileExist == "false":
            # Create socket on server
            c = socket(AF_INET, SOCK_STREAM)
    hostn = filename.replace("www.","",1)
    print hostn

    try:
        # Connect on port 80
        c.connect(hostn, 80)
        # Create temp file
        fileobj = c.makefile('r', 0)
        fileobj.write("GET " + "http://" + filename + "HTTP/1.0\n\n")

        # Read response into buffer
        tmpFile = open("./" + filename,"wb")
        for i in range(0, len(buff)):
            tmpFile.write(buff[i])
        clientSocket.send(buff[i])
    except:
        print("Illegal Request")
    else:
        print('404 Error - File note found')
           
clientSocket.close()
           
if __name__ == '__main__':
    main()
