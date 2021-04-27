from batfish import batfish

SRC_IP = "10.1.255.100"
# DST_IP = "10.3.255.100"
DST_IP = "8.8.8.8"
DST_PORT = "53"
APPLICATIONS = ["dns", "ssh"]
IP_PROTOCOLS = ["tcp", "udp"]

b = batfish(
    src_ip=SRC_IP,
    dst_ip=DST_IP,
    dst_port=DST_PORT,
    device_type=None,
    BATFISH_NETWORK=None,
    BATFISH_SERVER=None,
)
b.get_configs()
answers = b.get_data()