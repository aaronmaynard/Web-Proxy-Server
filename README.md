# Web-Proxy-Server
 A small web proxy server which is able to cache web pages. It is a very simple proxy server which only understands simple GET-requests, but is able to handle all kinds of objects - not just HTML pages, but also images.  The language used for implementation is Python 2.

### Compiling the Server
how you compile the server

### Running the Proxy Server
Run the proxy server program using your command prompt and then request a web page from your
browser. Direct the requests to the proxy server using your IP address and port number.
For e.g. http://localhost:5005/www.google.com

5005 is an arbitrarily chosen port number where the client can reach the proxy server. The only requirement is that the port number should not coincide with any of the reserved port numbers. To use the proxy server with browser and proxy on separate computers, you will need the IP address on which your proxy server is running. In this case, while running the proxy, you will have to replace the “localhost” with the IP address of the computer where the proxy server is running. Also note the port number used. You will replace the port number used here “5005” with the port number you have used in your server code at which your proxy server is listening.

### Hardware Setup
Available memory
Power management features
Devices that are connected such as modems, disc drives and serial ports
etc

### Configuring your Browser
You can also directly configure your web browser to use your proxy. This depends on your browser. In Internet Explorer, you can set the proxy in Tools > Internet Options > Connections tab > LAN Settings. In Netscape (and derived browsers such as Mozilla), you can set the proxy in Tools > Options > Advanced tab > Network tab > Connection Settings. In both cases you need to give the address of the proxy and the port number that you gave when you ran the proxy server. You should be able to run the proxy and the browser on the same computer without any problem. With this approach, to get a web page using the proxy server, you simply provide the URL of the page you want. For example: http://www.google.com

## Current update | 1:30 PM 7/24/2018
Bug Fixes - Ability to parse url file extensions.  Server running Python 2.7.10  
Sample Run:  

![TestRun](https://i.imgur.com/mBkvpVm.png)
