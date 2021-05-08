
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

start_node = "spoke1"
start_interface = "port4"
src_ip = "10.10.10.1"
destination_ip = "218.8.104.58"


@pytest.mark.batfish
def main():

    ac = AccessCheck()

    
    results = ac.check(src_ip=src_ip, destination_ip=destination_ip, snapshot_folder="/shared/data/storage/firewall-configs/snapshot")



    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)


## cast assertions
# disposition accepted?


class TraceResult:

    def __init__(self, traces=None, flow=None) -> None:
        pass

        self.traces = traces
        self.flow = flow
    




if __name__ == "__main__":
    main()