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

for dest in openport:
    service = socket.getservbyport(dest)
    print "port %d provides %s service" % (dest, service)

dnspck = sr1(IP(dst=dst_ip)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname="vital.nyu.poly:1113/vnc_auto.html"),verbose=0))
print dnspck[DNS].summary()

conf.checkIPadr = False
fam, hw = get_if_raw_hwaddr(conf.iface)
dhcp = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0",dst="25.255.255.255")/UDP(sport=68,dport=67)/BOOTP(chaddr=hw)/DHCP(options=[("message-type","discover"),"end"])
ans, uans = srp(dhcp,multi=True)
for p in ans:
    print p[1][Ether].src, p[1][IP].src

