import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import*

dst_ip = "10.10.111.1"
src_port = RandShort()
dst_ports = range(1,101)
open_or_dropped = []
openport = []
closedport = []

for dst_port in dst_ports:
    udp_res= sr1(IP(dst=dst_ip)/UDP(sport=src_port,dport=dst_port),timeout=10)
    if str(type(udp_res)) == "<type 'NoneType'>":
        open_or_dropped.append(dst_port)
        udp_res1 = sr1(IP(dst=dst_ip)/UDP(sport=src_port,dport=dst_port),timeout=5)
        if str(type(udp_res1)) == "<type 'NoneType'>":
            openport.append(dst_port)
    else:
        closedport.append(dst_port)

print "OPEN OR DROPPED: ", open_or_dropped
print "OPEN: ", openport
print "CLOSED: ", closedport
