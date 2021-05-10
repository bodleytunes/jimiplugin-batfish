
# Fudge the python path
import sys
import os

import pandas as pd
import pytest


PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.route_check import RouteCheck

start_node = "spoke1"
start_interface = "port4"
destination_ip = "8.8.8.8"


@pytest.mark.batfish
def main():

    rc = RouteCheck()

    ingress = f"@enter({start_node}[{start_interface}])"
    
    results = rc.check(ingress=ingress, destination_ip=destination_ip, snapshot_folder="/shared/data/storage/firewall-configs/snapshot")



    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)


    flow = results["Flow"]
    t_results = results["Traces"]

    walk_flow(flow)
    walk_traces(t_results)

def walk_flow(flow):
    print(f"Flow Source IP: {flow.srcIp}")
    print(f"Flow Dest IP: {flow.dstIp}")
    print(f"Flow IP protocol: {flow.ipProtocol}")
    print(f"Flow Ingress Node: {flow.ingressNode}")
    print(f"Flow Ingress VRF: {flow.ingressVrf}")

def walk_traces(t_results):

    for result in t_results:
        for trace in result:
            print(f"Trace dispostion: {trace.disposition}")
            for hop in trace:
                print(f"hop node: {hop.node}")
                for step in hop:
                    if step.action == "ORIGINATED":
                        print(f"step detail originating VRF: {step.detail.originatingVrf}")
                    elif step.action == "FORWARDED":
                        print(f"Arp IP: {step.detail.arpIp}")
                        print(f"Output Interface: {step.detail.outputInterface}")
                        for route in step.detail.routes:
                            # Put assertions in here?
                            print(f"Network: {route['network']}")
                            print(f"Next-hop: {route['nextHopIp']}")
                            print(f"by Protocol: {route['protocol']}")
                    elif step.action == "PERMITTED":
                        print(f"Filter: {step.detail.filter}")
                        print(f"Filter Type: {step.detail.filterType}")
                        print(f"Dest IP: {step.detail.flow.dstIp}")
                        print(f"Dest Port: {step.detail.flow.dstPort}")
                        print(f"Ingress Node: {step.detail.flow.ingressNode}")
                        print(f"Ingress Interface: {step.detail.flow.ingressInterface}")
                        print(f"Ingress VRF: {step.detail.flow.ingressVrf}")
                        print(f"IP Protocol: {step.detail.flow.ipProtocol}")
                        print(f"Source IP: {step.detail.flow.srcIp}")
                    elif step.action == "TRANSMITTED":
                        print(f"Output Interface: {step.detail.outputInterface}")
                    elif step.action == "EXITS_NETWORK":
                        print(f"Output Interface: {step.detail.outputInterface}")
                        print(f"Next-hop IP: {step.detail.resolvedNexthopIp}")


## cast assertions
# disposition accepted?


class TraceResult:

    def __init__(self, traces=None, flow=None) -> None:
        pass

        self.traces = traces
        self.flow = flow
    




if __name__ == "__main__":
    main()