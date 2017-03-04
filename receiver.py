import socket
import sys

if len(sys.argv) != 2:
    print "python receiver.py [PORTNUMBER]"

UDP_IP = ""
UDP_PORT = int(sys.argv[1])
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((UDP_IP,UDP_PORT))
buf = 1024
ack = 0
current_size = 0
percent = round(0,2)
can_receive = True

while True:
    data,addr = s.recvfrom(buf)

    if data:
        (file_name, total_size, seq) = data.split("|||")

        if str(seq) == str(ack):
            f = open("received_" + file_name,"wb")
            print str(current_size) + " / " + str(total_size) + " (current size / total size), " + str(percent) + "%"
            ack = (ack + 1) % 2
            s.sendto(str(ack),addr)
            break

s.settimeout(0.5)
count = 0
while True:
    if can_receive:
        try:
            if count == 10:
                print "eroor"
                break

            data,addr = s.recvfrom(buf)

            if not data:
                break

            seq = data[len(data)-1]
            data = data[0:len(data)-1]

            if (str(ack) != str(seq)):
                print "seq is not equal to ack"
                continue

            can_receive = False

        except:
            count += 1
            print "timed out"
            s.sendto(str(ack),addr)

    if not can_receive:
        f.write(data)
        current_size += len(data)
        percent = round(float(current_size) / float(total_size) * 100,2)
        print str(current_size) + " / " + str(total_size) + " (current size / total size), "  + str(percent) + "%"
        ack = (ack + 1) % 2
        count = 0
        s.sendto(str(ack),addr)
        can_receive = True

f.close()
s.close()
if count < 10:
    print "File Donwloaded"
