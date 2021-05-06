
# Fudge the python path
import sys
import os

import pandas as pd


PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path


from plugins.batfish.includes.route_check import RouteCheck

start_node = "spoke1"
start_interface = "port4"

def main():

    rc = RouteCheck()

    ingress = f"@enter({start_node}[{start_interface}])"
    
    result = rc.check(ingress=ingress, destination_ip="8.8.8.8", snapshot_folder="/shared/data/storage/firewall-configs/snapshot")

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)
    
    print(result["Flow"][0])
    print(result["Traces"][0][0][0][0])















if __name__ == "__main__":
    main()