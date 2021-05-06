
# Fudge the python path
import sys
import os

import pandas as pd

PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.ip_owners import IpOwners

def main():

    

    i = IpOwners()

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)


    r = i.get_ip_owners(snapshot_folder="/shared/data/storage/firewall-configs/snapshot")
    
    print(r)










if __name__ == "__main__":
    main()