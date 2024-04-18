# TCP IP Model - Workflow

TCP-IP Model is simlar to OSI Model

- However the three layers 5,6 and 7 are combined to a Single Layer called Application Layer as these are more or less same component and performed by the Browser.
- Network layer is named as Internet Layer.
- Physical Layer and Data Link Layer are combined to a Single Layer called Network Interface Layer.

Let's break down the process of accessing Google.com using the TCP/IP model:

1. **Application Layer**:
   
   - The user types "Google.com" into their web browser (e.g., Chrome, Firefox).
   - The browser initiates a request to access Google.com, utilizing the HTTP (Hypertext Transfer Protocol) at the application layer.
2. **Transport Layer**:
   
   - The browser sends the HTTP request to the Transport Layer, where it is divided into smaller packets by the Transmission Control Protocol (TCP). TCP is responsible for ensuring reliable and ordered delivery of data between the client (user's computer) and the server (Google's server).
   - TCP establishes a connection with Google's server using a three-way handshake: SYN, SYN-ACK, and ACK.
3. **Internet Layer (Network Layer)**:
   
   - The TCP segments are then encapsulated into IP (Internet Protocol) packets at the Network Layer. Each packet contains the source and destination IP addresses.
   - The IP packets are routed through the Internet using routers. They are forwarded based on the destination IP address until they reach Google's server.
4. **Link Layer (Data Link Layer)**:
   
   - At the Link Layer, the IP packets are further encapsulated into frames, which contain physical addresses (MAC addresses) of the source and destination devices.
   - The frames are then transmitted over the physical network infrastructure, such as Ethernet or Wi-Fi, using switches or access points.
5. **Physical Layer**:
   
   - Finally, the frames are converted into electrical signals (in wired networks) or radio waves (in wireless networks) and transmitted over the physical medium (e.g., cables, air).

Upon reaching Google's server, the process is reversed:

1. The physical layer receives the signals and converts them into frames.
2. The link layer removes the frames and extracts the IP packets.
3. The network layer routes the IP packets to the appropriate destination.
4. The transport layer receives the TCP segments, reassembles them into the original HTTP request, and delivers it to the web server.
5. The application layer processes the HTTP request, retrieves the requested web page (in this case, Google.com), and sends it back to the user's browser as an HTTP response.

Throughout this process, each layer of the TCP/IP model performs specific functions to ensure that data is transmitted reliably and efficiently between the user's device and Google's server.

