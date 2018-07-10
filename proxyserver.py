import socket


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
    #wait for a connection
    print('WEB PROXY SERVER IS LISTENING')
    
    #accept() returns a new connection socket along with the address
    clientSocket, clientAddress = welcomeSocket.accept()
    print('WEB PROXY SERVER CONNECTED WITH ' + str(clientAddress))
    print('MESSAGE RECEIVED FROM CLIENT:')
    request = clientSocket.recv(2048)
    print(request)
    # Parse Request 
    header = request.split("\n")[0].split(" ")
    for x in header:
        print(x)
    # Get HTTP Command    
    command = header[0]
    
    print(header[1].split('/'))

    if(command == 'GET'):
        # check cache
        # open socket and send request if object not in cache
        
        # get website the browser is trying to access
        # port 80 for HTTP
        address = (header[1].split('/')[1], 80)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        
    clientSocket.close()

    
