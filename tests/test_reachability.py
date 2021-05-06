
# Fudge the python path
import sys
import os

import pandas as pd


PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path


from plugins.batfish.includes.reachability_check import ReachabilityCheck

start_node = "spoke1"
start_interface = "port4"

def main():

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)


    rc = ReachabilityCheck()

    
    result = rc.check(start_location="spoke1", destination_ip="8.8.8.8", snapshot_folder="/shared/data/storage/firewall-configs/snapshot")

    print(result)









if __name__ == "__main__":
    main()