import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import*

dst_ip = "10.10.111.1"
dst_ports = range(1,101)
src_port = RandShort()
openport = []
closedport = []
filteredport = []

for dst_port in dst_ports:
    tcp_res=sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags='S'),timeout=10)
    if str(type(tcp_res)) == "<type 'NoneType'>":
        tcp_res1=sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags='S'),timeout=5)
        if str(type(tcp_res1)) == "<type 'NoneType'>":
            filteredport.append(dst_port)
        elif tcp_res1.haslayer(TCP):
            if tcp_res1.getlayer(TCP).flags == 0x12:
                rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags='AR'),timeout=5)
                openport.append(dst_port)
            elif tcp_res1.getlayer(TCP).flags == 0x14:
                closedport.append(dst_port)
     elif tcp_res.haslayer(TCP):
         if tcp_res.getlayer(TCP).flags == 0x12:
             rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags='AR'),timeout=5)
             openport.append(dst_port)
         elif tcp_res.getlayer(TCP).flags == 0x14:
             closedport.append(dst_port)

print "OPEN: ", openport
print "CLOSED: ", closedport
print "FILTERED: ", filteredport


             
