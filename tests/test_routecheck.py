# Fudge the python path
import sys
import os

import pandas as pd
import pytest


PACKAGE_PARENT = "../../../"
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.trace_route_check import TraceRouteCheck
from plugins.batfish.includes.batfish import Batfish
from plugins.batfish.includes.result_models.traceroute import DataviewTraceroute


start_node = "spoke1"
start_interface = "port4"
destination_ip = "172.16.2.4"


@pytest.mark.batfish
def main():

    b = Batfish()

    b.init_batfish(
        snapshot_folder="/shared/data/storage/firewall-configs/snapshot",
    )

    rc = TraceRouteCheck(b_fish=b)

    ingress = f"@enter({start_node}[{start_interface}])"

    results = rc.check(
        ingress=ingress,
        destination_ip=destination_ip,
        snapshot_folder="/shared/data/storage/firewall-configs/snapshot",
    )

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)

    # separate out Flow and Traces
    flow = results.iloc[0]["Flow"]
    traces = results.iloc[0]["Traces"]

    walk_flow(flow)
    walk_traces(traces)


def walk_flow(flow):
    print(f"Flow Source IP: {flow.srcIp}")
    print(f"Flow Dest IP: {flow.dstIp}")
    print(f"Flow IP protocol: {flow.ipProtocol}")
    print(f"Flow Ingress Node: {flow.ingressNode}")
    print(f"Flow Ingress VRF: {flow.ingressVrf}")


def walk_traces(traces):
    dvt_list = []

    for trace in traces:
        print(f"Trace dispostion: {trace.disposition}")
        # create new dataview traceroute
        dvt = DataviewTraceroute()

        for hop in trace:
            print(f"hop node: {hop.node}")
            dvt.hop_node = hop.node
            for step in hop:
                if step.action == "ORIGINATED":
                    print(f"step detail originating VRF: {step.detail.originatingVrf}")
                    dvt.originating_vrf = step.detail.originatingVrf
                elif step.action == "FORWARDED":
                    print(f"Arp IP: {step.detail.arpIp}")
                    dvt.arp_ip = step.detail.arpIp
                    print(f"Output Interface: {step.detail.outputInterface}")
                    dvt.output_interface = step.detail.outputInterface
                    for route in step.detail.routes:
                        # Put assertions in here?
                        print(f"Network: {route['network']}")
                        dvt.network = route["network"]
                        print(f"Next-hop: {route['nextHopIp']}")
                        dvt.next_hop_ip = route["nextHopIp"]
                        print(f"by Protocol: {route['protocol']}")
                        dvt.via_protocol = route["nextHopIp"]
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
                    dvt.output_interface = step.detail.outputInterface
                    print(f"Next-hop IP: {step.detail.resolvedNexthopIp}")
                    dvt.resolved_next_hop_ip = step.detail.resolvedNexthopIp
        # append dataview traceroute to list
        dvt_list.append(dvt)


## cast assrtions
# disposition accepted?


class TraceResult:
    def __init__(self, traces=None, flow=None) -> None:
        pass

        self.traces = traces
        self.flow = flow


if __name__ == "__main__":
    main()
