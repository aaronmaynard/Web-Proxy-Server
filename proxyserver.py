from socket import *
import sys
import re
import os

if len(sys.argv) <= 1:
  print 'Usage : "python proxyserver.py server_ip"\n[server_ip : Address of the proxy server'
#sys.exit(2)

# buffer size
BUFFER_SIZE = 65536

#port number is arbituary
welcomePort = 5005
try:
    #create welcoming socket
    welcomeSocket = socket(AF_INET, SOCK_STREAM)

    #bind to the server address
    welcomeSocket.bind(("", welcomePort))

    #begin listening (argument is number of allowed queued connections)
    welcomeSocket.listen(5)


#listening loop
    while True:
        # Start receiving data from client
        print('WEB PROXY SERVER IS LISTENING')
        
        # Accept() returns a new connection socket along with the address
        clientSocket, clientAddress = welcomeSocket.accept()
        print('WEB PROXY SERVER CONNECTED WITH ' + str(clientAddress))

        # wait 1 second to hear from client
        try:
            clientSocket.settimeout(1.0)
            request = clientSocket.recv(BUFFER_SIZE)
        except timeout:
            clientSocket.shutdown(SHUT_RDWR)
            clientSocket.close()
            continue 
        # do not parse empty message
        if(len(request) > 0):
            print('MESSAGE RECEIVED FROM CLIENT:')
            print(request)
            print 'END OF MESSAGE RECEIVED FROM CLIENT' 
        else:
            clientSocket.shutdown(SHUT_RDWR)
            clientSocket.close()
            continue 
        # Parse Request
        method = request.split(" ")[0]
        url = request.split(" ")[1]
        writefile = True
        # See if the URL contains a file 
        filematcher = re.compile("((.?)*\.[a-z]*$)")
        fmatch = filematcher.match(url)
        if (fmatch):
            filename = url.split('/')[-1]
            if filename in os.listdir("."):
                # Cache Hit
                print 'Cache Hit'
                # Assemble HTTP response 
        else:
            writefile = False
            # check the immediate directory for that file
            
        

        print '[PARSE MESSAGE HEADER]:'
        print 'METHOD = ' + str(request.split()[0]) + ', DESTADDRESS = ' + str(request.split()[1]) + ', HTTPVersion = ' + str(request.split()[2])
        
#        print request.split()[1]
#        filename = request.split()[1].partition("/")[2]
#        print filename
#        fileExist = "false"
        filetouse = str(request.split()[1]).replace('/', '_')
        print filetouse
#        print request.split()[4]
#        hostIP = gethostbyname(request.split()[4])
#        print hostIP
#
        # Check if file is already in cache
       # 
       # try:
       #     f = open(filetouse[1:0], "r")
       #     outputdata = f.readlines()
       #     fileExist = "true"
       #     # Cache is found
       #     clientSocket.send("HTTP/1.0 200 OK\r\n")
       #     clientSocket.send("Content-Type:text/html\r\n")
       #     for i in range(0, len(outputdata)):
       #         clientSocket.send(outputdata[i])
       #     print ('Read from cache')

       # # Error handling E404
       # except IOError:
       #     if fileExist == "false":
       #         # Create socket on server
       #         c = socket(AF_INET, SOCK_STREAM)
       # hostn = filename.replace("www.","",1)
       # print hostn
        
        try:
            forwardSocket = socket(AF_INET, SOCK_STREAM)
            # Connect on port 80
            hostIP = gethostbyname(request.split()[4])
            address = (hostIP, 80)
            forwardSocket.connect(address)
            forwardSocket.send(request)
            # keep reading and forwarding until nothing server stops
            if(writefile):
                with open(filename, 'w') as file:                
                    while True:
                        forwardSocket.settimeout(1.0)
                        response = forwardSocket.recv(BUFFER_SIZE)
                        if(len(response) > 0):
                            #data = "\r".join(response[response.split('\r').index('\n'):])
                            try:
                                #dataIndex = response.split('\r').index('\n')                                
#                                data = response.split('\r')[dataIndex:]
                                #data = response.split('\f\f')[1]
                                #file.writelines(data)
                                print response.split('\r\n')[:2]
                                data = response.split('\r\n')[2:]
                                file.writelines(data)
                                clientSocket.send(response)
                            except IndexError:
                                print "Value Error"
                                print response
                                file.write(response)
                                clientSocket.send(response)
                        else:
                            break
            else:
                while True:
                        forwardSocket.settimeout(1.0)
                        response = forwardSocket.recv(BUFFER_SIZE)
    
                        if(len(response) > 0):
                            clientSocket.send(response)
                        else:
                            break
            forwardSocket.close()
            clientSocket.close()
#            if "chunked" in response.split('\n')[4].split()[1]:
#                with open(".buffer", 'w') as buff:
#                    chunked = True
#                    while(chunked):
#                        print response
#                        buff.writelines(response.split('\n')[9:])
#                        forwardSocket.send(request)
#                        response = forwardSocket.recv(BUFFER_SIZE)
#                        print response.split('\n')[4]
#                        if "chunked" in response.split('\n')[4]:
#                            chunked = True
#                        else:
#                            chunked = False
#            else:
#                print response
#                clientSocket.send(response)
            # Create temp file
#            fileobj = c.makefile('r', 0)
#            fileobj.write("GET " + "http://" + filename + "HTTP/1.0\n\n")

            # Read response into buffer
#            tmpFile = open("./" + filename,"wb")
#            for i in range(0, len(buff)):
#                tmpFile.write(buff[i])
#            clientSocket.send(buff[i])
        except timeout:
            forwardSocket.close()
            clientSocket.close()
        except Exception as e:
            print(e)
            print("Illegal Request")
       # else:
   #     print('404 Error - File note found')
except KeyboardInterrupt:
    print 'Exiting Gracefully'
    welcomeSocket.shutdown(SHUT_RDWR)
    welcomeSocket.close()
    sys.exit()
           
if __name__ == '__main__':
    main()
