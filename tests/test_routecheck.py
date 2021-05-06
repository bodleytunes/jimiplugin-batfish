
# Fudge the python path
import sys
import os

import pandas as pd


PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.route_check import RouteCheck

def main():

    rc = RouteCheck()
    
    result = rc.check_route(start_ip="@enter(hub1[port4])", destination_ip="8.8.8.8", snapshot_folder="/shared/data/storage/firewall-configs/snapshot")

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)

    print(result)

    #next_hops = result["next_hops"]
    #egress_ifaces = result["egress_iface"]
#
    #for nh in next_hops:
    #    print(f"Next hop is: {nh}")
    #
    #for iface in egress_ifaces:
    #    print(f"egress iface: {iface}")















if __name__ == "__main__":
    main()