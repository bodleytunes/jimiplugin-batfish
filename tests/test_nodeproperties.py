
# Fudge the python path
import sys
import os

import pandas as pd

PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.node_properties import NodeProperties

def main():

    

    np = NodeProperties()

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)


    result = np.check_node_properties(snapshot_folder="/shared/data/storage/firewall-configs/snapshot")
    
    print(result["Node"])










if __name__ == "__main__":
    main()