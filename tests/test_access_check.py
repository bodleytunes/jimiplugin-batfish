
# Fudge the python path
import sys
import os

import pandas as pd
import pytest


PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.access_check import AccessCheck

src_ip = "10.1.255.100"
destination_ip = "10.3.255.100"
#applications =["dns"]
applications =["icmp"]
nodes = "spoke2"


@pytest.mark.batfish
def main():

    ac = AccessCheck()

    
    results = ac.check(src_ip=src_ip, destination_ip=destination_ip, applications=applications, nodes=nodes, snapshot_folder="/shared/data/storage/firewall-configs/snapshot")



    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)

    #print(results.values)
    for v in results.values:
        for a in v:
            for enum, e in enumerate(v):
                if enum == 0:
                    print(f"Node Queried is {e}")
                if enum == 1:
                    print(f"From zone/iface to zone/iface {e}")
                if enum == 2:
                    print(f"Flow details: {e}")
                if enum == 3:
                    print(f"Flow result : *** {e} ***")
                if enum == 4:
                    pass
                if enum == 5:
                    print(f"TraceTreeList: {e}")
            


## cast assertions
# disposition accepted?


class TraceResult:

    def __init__(self, traces=None, flow=None) -> None:
        pass

        self.traces = traces
        self.flow = flow
    




if __name__ == "__main__":
    main()