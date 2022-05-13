import socket
import struct
import time
from contextlib import closing
UDP_IP="192.168.43.41"
UDP_PORT=9000

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
sock.bind((UDP_IP,UDP_PORT))

count =0

with closing(sock):
   while True:
       count +=1
       data,addr = sock.recvfrom(1024)
       print("Send from ESP",addr,"-",data)
       time.sleep(1)
       #sock .sendto(b'hello\0',addr)
       mes = (str(count)+'\0').encode()
       sock.sendto(mes,addr)