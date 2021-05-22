# Fudge the python path
import sys
import os

PACKAGE_PARENT = "../../../../"
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path


from plugins.batfish.includes.queries.query import PortAccessQuery, BatfishQuery


def main():
    p = PortAccessQuery()
    p.port = "80"
    p.src_ip = "10.3.255.100"
    p.dst_ip = "172.16.4.2"

    b = BatfishQuery(a=p)
    b.nodes = ["spoke1"]
    # p = PortAccessQuery(src_ip="10.3.255.100", dst_ip="172.16.4.2", dst_ports="80")
    print(b)


if __name__ == "__main__":
    main()
