from socket import *
import sys
import re
import os
import httplib

def createRequest(host, url, originalRequest):
    try:
        hostInd = url.index(host)
        url = url[hostInd + len(host):]
    except ValueError:
        pass
    httpHeader = "GET " + url + " HTTP/1.1\r\n"
    httpHeader += ("Host: " + host + '\r\n')
    httpHeader += "Connection: close\r\n"
    
    for line in originalRequest.split('\r\n'):
        if 'User-Agent' in line:
            httpHeader += (line + '\r\n')
        if 'Accept:' in line:
            httpHeader += (line + '\r\n')
        if 'Referer:' in line:
            httpHeader += (line + '\r\n')
        if 'Accept-Encoding:' in line:
            httpHeader += (line + '\r\n')
        if 'Accept-Language:' in line:
            httpHeader += (line + '\r\n')
        if 'Cookie:' in line:
            httpHeader += (line + '\r\n')
    httpHeader += '\r\n\r\n'
    return httpHeader


if len(sys.argv) <= 1:
  print 'Usage : "python proxyserver.py server_ip"\n[server_ip : Address of the proxy server'
#sys.exit(2)

serverIP = sys.argv[1]

# buffer size
BUFFER_SIZE = 65536

#port number is arbituary
welcomePort = 5005
encodeFlag = []
encodeDict = {}
try:
    #create welcoming socket
    welcomeSocket = socket(AF_INET, SOCK_STREAM)

    #bind to the server address
    welcomeSocket.bind((serverIP, welcomePort))

    #begin listening (argument is number of allowed queued connections)
    welcomeSocket.listen(5)


#listening loop
    while True:
        # Start receiving data from client
        print('WEB PROXY SERVER IS LISTENING')
        
        # Accept() returns a new connection socket along with the address
        clientSocket, clientAddress = welcomeSocket.accept()
        print('WEB PROXY SERVER CONNECTED WITH ' + str(clientAddress))

        # wait 100ms second to hear from client
        try:
            clientSocket.settimeout(0.1)
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
        
        # Parse Request Header
        
        method = request.split(" ")[0]
        url = request.split(" ")[1]
       # url = url[1:]
        try:
            domainIndex = url.index('.')
            host = url[:domainIndex+4]
        except ValueError:
            pass
        for line in request.split('\r\n'):
            if "Referer:" in line:
                temp = line.split(" ")[1]
                temp = temp.split(':'.join([str(serverIP), str(welcomePort)]))[1]
                domIndex = temp.find(".")
                host = temp[1:domIndex+4]
        
        print '[PARSE MESSAGE HEADER]:'
        print 'METHOD = ' + method + ', DESTADDRESS = ' + url + ', HTTPVersion = ' + str(request.split()[2])
        
        # Discard serverIP:welcomePort
#        try:
#            url = url.split(':'.join([str(serverIP), str(welcomePort)]))[1]
#            # extract host from the remaining URL
#            print url
#        except IndexError:
#            # browser is not putting serverIP:welcomePort into the URL 
#            # keep going 
#            pass
        
        
        writefile = True
        # See if the URL contains a filename 
        filematcher = re.compile("((.?)*\.(jpg|htm|html|png|ico|js|css|gif)$)")
        fmatch = filematcher.match(url)
        if (fmatch):
            filename = url.split('/')[-1]
            if filename in os.listdir("."):
                # Cache Hit
                print 'Cache Hit'
                # Assemble HTTP response 
                httpHeader = 'HTTP/1.1 200 OK\r\n'
                if '.jpg' in filename:
                    httpHeader += 'Content-Type: image/jpeg\r\n'
                elif 'html' or 'htm' in filename:
                    httpHeader += 'Content-Type: text/html\r\n'
                elif '.ico' in filename:
                    httpHeader += 'Content-Type: image/x-icon\r\n'
                elif '.css' in filename:
                    httpHeader += 'Content-Type: text/css\r\n'
                elif '.js' in filename:
                    httpHeader += 'Content-Type: application/javascript\r\n'
                elif '.txt' in filename:
                    httpHeader += 'Content-Type: text/plain\r\n'
                else:
                    httpHeader += 'Content-Type: application/octet-stream\r\n'
                
                # See if it was sent using special encoding
                
                if filename in encodeFlag:
                    httpHeader += (encodeDict[filename] + '\r\n') 
                
                httpHeader += '\r\n\r\n'
                
                print 'HTTP Header sent to Client:'
                print httpHeader
                # Add the file data
                with open(filename, 'r') as file:
                    # Reading the whole file until it doesn't work 
                    data = file.read()
                    httpHeader += data
                clientSocket.send(httpHeader)
                clientSocket.close()
                continue                                        
        else:
            writefile = False
            url = "Http://" + url
            # if here then the request was not for a specific file (metadata?)
            
        


#        print request.split()[1]
#        filename = request.split()[1].partition("/")[2]
#        print filename
#        fileExist = "false"
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

# Cache miss must send request to original destination
        
        try:
            forwardSocket = socket(AF_INET, SOCK_STREAM)
            # Connect on port 80
            hostIP = gethostbyname(host)
            address = (hostIP, 80)
            forwardSocket.connect(address)
            newRequest = createRequest(host, url, request)
            print 'REQUEST MESSAGE SENT TO ORIGINAL SERVER:'
            print newRequest
            print 'END OF MESSAGE SENT TO ORIGINAL SERVER.'
            forwardSocket.send(newRequest)
            # keep reading and forwarding until nothing server stops
            if(writefile):
                with open(filename, 'w') as file:                
                    while True:
                        forwardSocket.settimeout(0.5) # 500ms
                        response = forwardSocket.recv(BUFFER_SIZE)
                        if(len(response) > 0):
                            #data = "\r".join(response[response.split('\r').index('\n'):])
                            try:
#                                dataIndex = response.split('\n').index('\r')                                
#                                data = response.split('\r')[dataIndex+1:]
                                # drop the line feed 
#                                data[0] = data[0][1:]
#                                data = response
                                # remove the header
#                                textMatcher = re.compile("(.?)*\.(js|css|html)$")
#                                textMatch = textMatcher.match(filename)
#                                if textMatch:
#                                    print response             
                                if 'HTTP' in response.split('\r\n\r\n')[0]:
                                    temp = response.split('\r\n\r\n')
                                    header = temp[0]
                                    print 'RESPONSE HEADER FROM ORIGINAL SERVER'
                                    print header
                                    print 'END OF HEADER'
                                    print '[WRITE FILE INTO CACHE]: ' + filename
                                    if len(temp) < 3:
                                        data = temp[1]
                                    else:
                                        data = '\r\n\r\n'.join(temp[1:])
                                    file.write(data)
                                else:
                                    file.write(data)
                                # See if there is special encoding to note
                                
                                for line in response.split('\r\n'):
                                    if 'Content-Encoding:' in line:
                                        encodeFlag.append(filename)
                                        encodeDict[filename] = line
                                
#                                data = response.split('\r\n')[2:]
#                                file.writelines(data)
                                clientSocket.send(response)
                            except IndexError:
#                                print "*********Value Error***********"
#                                print response
#                                print response.split('\n')
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
            print 'timeout'
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


