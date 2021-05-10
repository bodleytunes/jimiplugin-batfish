
# Fudge the python path
import sys
import os

import pandas as pd
import pytest
import re


PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.access_check import AccessCheck

src_ip = "10.1.255.100"
destination_ip = "10.3.255.100"
#applications =["dns"]
applications =["icmp"]
nodes = "spoke1"
node_list = ["spoke1", "spoke2"]


@pytest.mark.batfish
def main():

    ac = AccessCheck()

    
    results = ac.check(src_ip=src_ip, destination_ip=destination_ip, applications=applications, nodes=nodes, snapshot_folder="/shared/data/storage/firewall-configs/snapshot")
    all_results = []
    for node in node_list:
        all_results.append(ac.check(src_ip=src_ip, destination_ip=destination_ip, applications=applications, nodes=node, snapshot_folder="/shared/data/storage/firewall-configs/snapshot"))

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)

    #show_all(results)
    show_permitted(results)
    #show_denied(results)
    show_permitted_all(all_results)



def show_all(results):
    # print all results
    for v in results.values:
        for a in v:
            for enum, e in enumerate(v):
                if enum == 0:
                    print(f"Node Queried is: {e}")
                if enum == 1:
                    print(f"From zone/iface to zone/iface: {e}")
                if enum == 2:
                    print(f"Flow details: {e}")
                if enum == 3:
                    print(f"Flow result : *** {e} ***")
                if enum == 4:
                    pass
                if enum == 5:
                    print(f"TraceTreeList: {e}")

            

def show_permitted(results):

    # print only if accepted/permitted
    for v in results.values:
        if re.search("permit", v[3], re.IGNORECASE):
            if len(v[5]) > 0:
                for item in v[5]:
                    for item_child in item.children:
                        for c in item_child.children:
                            if re.search('permitted', c.traceElement.fragments[0].text, re.IGNORECASE):
                                for enum, e in enumerate(v):
                                    if enum == 3:
                                        print("========================")
                                        print(f"Flow result : *** {e} ***")
                                        continue
                                    if enum == 0:
                                        print(f"Node Queried is: {e}")
                                    if enum == 1:
                                        print(f"From zone/iface to zone/iface: {e}")
                                    if enum == 2:
                                        print(f"Flow details: {e}")
                                    if enum == 4:
                                        pass
                                    if enum == 5:
                                        print(f"TraceTreeList: {e}")
                                        print("========================")

def show_permitted_all(all_results):

    # print only if accepted/permitted
    for result in all_results:
        for v in result.values:
            if re.search("permit", v[3], re.IGNORECASE):
                if len(v[5]) > 0:
                    for item in v[5]:
                        for item_child in item.children:
                            for c in item_child.children:
                                if re.search('permitted', c.traceElement.fragments[0].text, re.IGNORECASE):
                                    for enum, e in enumerate(v):
                                        if enum == 3:
                                            print("========================")
                                            print(f"Flow result : *** {e} ***")
                                            continue
                                        if enum == 0:
                                            print(f"Node Queried is: {e}")
                                        if enum == 1:
                                            print(f"From zone/iface to zone/iface: {e}")
                                        if enum == 2:
                                            print(f"Flow details: {e}")
                                        if enum == 4:
                                            pass
                                        if enum == 5:
                                            print(f"TraceTreeList: {e}")
                                            print("========================")

def show_denied(results):

    # print only if accepted/permitted
    for v in results.values:
        if "DENY" in v[3]:
            for enum, e in enumerate(v):
                if enum == 3:
                    print(f"Flow result : *** {e} ***")
                    continue
                if enum == 0:
                    print(f"Node Queried is: {e}")
                if enum == 1:
                    print(f"From zone/iface to zone/iface: {e}")
                if enum == 2:
                    print(f"Flow details: {e}")
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