#!/bin/python3

import sys
import socket
from datetime import datetime

#defining the target
if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1]) #translate hostname to IPv4

else:
    print("Invalid amount of arguments")

print("\n")
print("Scanning target: ", target)
print("Time started :",str(datetime.now()))
print("\n")

try:
    for port in range(50,85):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        reset = s.connect_ex((target,port))
        if reset == 0:
            print(f"Port {port} is open")
        s.close()               #attempting to scan home router
except KeyboardInterrupt:
    print("\n Exiting program.")
    sys.exit()
except socket.gaierror:
    print("Hostname could not be resolved. ")
    sys.exit()
except socket.error:
    print("Could not connect to server")
    sys.exit()
