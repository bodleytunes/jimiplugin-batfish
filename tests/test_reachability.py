
# Fudge the python path
import sys
import os

import pandas as pd
import pytest


PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.reachability_check import ReachabilityCheck

start_location = "spoke1"
destination_ip = "8.8.8.8"


@pytest.mark.batfish
def main():

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)

    rc = ReachabilityCheck()
    
    result = rc.check(start_location=start_location, destination_ip=destination_ip, snapshot_folder="/shared/data/storage/firewall-configs/snapshot")
    flow = result.iloc[0]['Flow']
    traces = result.iloc[0]['Traces']


    t_result = TraceResult(traces=traces, flow=flow)

    #print(result.to_string())
    #print("Flow")
    #print(t_result.flow)
#
    #print("Traces")
    #print(t_result.traces)
#
    traces = t_result.traces

    walk_traces(traces)


def walk_traces(traces):

    for trace in traces:
        print(f"Trace dispostion: {trace.disposition}")
        for hop in trace:
            print(f"hop node: {hop.node}")
            for step in hop:
                if step.action == "ORIGINATED":
                    print(f"step detail originating VRF {step.detail.originatingVrf}")
                elif step.action == "FORWARDED":
                    print(f"Arp IP: {step.detail.arpIp}")
                    print(f"Output Interface: {step.detail.outputInterface}")
                    for route in step.detail.routes:
                        print(f"Network {route['network']}")
                        print(f"Next-hop {route['nextHopIp']}")
                        print(f"by Protocol {route['protocol']}")
                



class TraceResult:

    def __init__(self, traces=None, flow=None) -> None:
        pass

        self.traces = traces
        self.flow = flow
    
    
  

if __name__ == "__main__":
    main()