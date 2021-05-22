# Fudge the python path
import sys
import os

PACKAGE_PARENT = "../../../../"
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path


from plugins.batfish.includes.queries.query import (
    PortAccessQuery,
    BatfishQuery,
    ProtocolAccessQuery,
)


def main():
    port_query = PortAccessQuery()
    port_query.port = "80"
    port_query.src_ip = "10.3.255.100"
    port_query.dst_ip = "172.16.4.2"

    proto_query = ProtocolAccessQuery()
    proto_query.protocol = "icmp"
    proto_query.src_ip = "10.3.255.100"
    proto_query.dst_ip = "172.16.4.2"

    b1 = BatfishQuery(a=port_query)
    b1.nodes = ["spoke1"]

    b2 = BatfishQuery(a=proto_query)
    b2.nodes = ["spoke1"]
    # p = PortAccessQuery(src_ip="10.3.255.100", dst_ip="172.16.4.2", dst_ports="80")
    print(b1)
    print(b2)


if __name__ == "__main__":
    main()
