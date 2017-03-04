import socket
import sys
import os

if len(sys.argv) != 4:
    print "python sender.py [IPADDRESS] [PORTNUMBER] [FILENAME]"
    sys.exit()

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
Server_IP = sys.argv[1]
Server_Port = int(sys.argv[2])
buf = 1024
addr = (Server_IP,Server_Port)
seq = 0
ack = 0
file_name=sys.argv[3]
total_size = os.path.getsize(file_name)
current_size = 0
percent = round(0,2)
f = open(file_name,"rb") 

data = str(file_name) + "|||" + str(total_size) + "|||" + str(seq)

while True:
    s.sendto(data,addr)
    seq = (seq + 1) % 2

    s.settimeout(0.5)
    count = 0
    while True:
        try:
            if count == 10:
                print "error"
                break

            ack,addr = s.recvfrom(buf)

            if (str(ack) == str(seq)):
                print str(current_size) + " / " + str(total_size) + "(current size / total size), " + str(percent) + "%"
                break
            else:
                print "ack is not equal to seq"

        except:
            count += 1
            print "timed out"
            s.sendto(data,addr)
	
    if count == 10:
        break

    data = f.read(buf-1)
    current_size += len(data)
    percent = round(float(current_size) / float(total_size) * 100,2)
    if not data:
        s.sendto("",addr)
        break
    data = data + str(seq)

s.close()
f.close()
