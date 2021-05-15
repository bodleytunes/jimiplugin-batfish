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

from plugins.batfish.includes.reachability_check import ReachabilityCheck
from plugins.batfish.includes.batfish import Batfish


class ReachabilityResult:
    def __init__(
        self,
    ):
        self.flow_result: FlowResult = None
        self.trace_result: list[TraceResult] = []

        pass


class FlowResult(ReachabilityResult):
    def __init__(
        self,
        src_ip=None,
        dst_ip=None,
        ip_protocol=None,
        ingress_node=None,
        ingress_vrf=None,
    ):

        self.src_ip = src_ip


# class TraceResult(ReachabilityResult):
class TraceResult(ReachabilityResult):
    def __init__(
        self,
    ):

        self.trace_disposition: str
        self.hops: list[Hop] = []


class Hop(TraceResult):
    def __init__(
        self,
    ):

        self.node: str
        self.steps: list[Step] = []


class Step(Hop):
    def __init__(
        self,
    ):

        self.action: str
        self.details: list[Detail] = []


class Detail(Step):
    def __init__(
        self,
    ):

        self.originating_vrf: str
        self.arp_ip: str
        self.output_interface: str
        self.routes: list[Route] = []
        self.filter: str
        self.filter_type: str
        self.resolve_next_hop: str
        self.flow = Flow()


class Route(Detail):
    def __init__(
        self,
    ):
        self.network: str
        self.next_Hop: str
        self.via_protocol: str
        pass


class Flow(Detail):
    def __init__(
        self,
    ):
        self.src_ip: str
        self.dst_ip: str
        self.dst_port: str
        self.ingress_node: str
        self.ingress_interface: str
        self.ingress_vrf: str
        self.ip_protocol: str

        pass


start_location = "spoke1"
destination_ip = "172.16.4.2"


@pytest.mark.batfish
def main():

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)

    b = Batfish()

    b.init_batfish(
        snapshot_folder="/shared/data/storage/firewall-configs/snapshot",
    )

    rc = ReachabilityCheck(b_fish=b)

    result = rc.check(
        start_node=start_location,
        destination_ip=destination_ip,
    )

    # separate out Flow and Traces
    flow = result.iloc[0]["Flow"]
    traces = result.iloc[0]["Traces"]

    rr = ReachabilityResult()

    walk_flow(flow, rr)
    walk_traces(traces, rr)


def walk_flow(flow, rr):
    print(f"Flow Source IP: {flow.srcIp}")
    print(f"Flow Dest IP: {flow.dstIp}")
    print(f"Flow IP protocol: {flow.ipProtocol}")
    print(f"Flow Ingress Node: {flow.ingressNode}")
    print(f"Flow Ingress VRF: {flow.ingressVrf}")

    rr.flow_result = FlowResult()

    rr.flow_result.src_ip = flow.srcIp
    rr.flow_result.dst_ip = flow.dstIp
    rr.flow_result.ip_protocol = flow.ipProtocol
    rr.flow_result.ingress_node = flow.ingressNode
    rr.flow_result.ingress_vrf = flow.ingressVrf

    print("hello")


def walk_traces(traces, rr):

    tr = TraceResult()

    for trace in traces:
        print(f"Trace dispostion: {trace.disposition}")

        tr.trace_disposition = trace.disposition

        for hop in trace:
            print(f"hop node: {hop.node}")

            tr.hops = [Hop()]

            for enum, step in enumerate(hop):

                new_step = Step()
                new_detail = Detail()
                new_route = Route()

                if step.action == "ORIGINATED":
                    print(f"step detail originating VRF: {step.detail.originatingVrf}")
                    # add to detail
                    new_detail.originating_vrf = step.detail.originatingVrf

                elif step.action == "FORWARDED":
                    print(f"Arp IP: {step.detail.arpIp}")
                    new_detail.arp_ip = step.detail.arpIp
                    print(f"Output Interface: {step.detail.outputInterface}")
                    new_detail.output_interface = step.detail.outputInterface

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

                # append stuff
                new_step.details.append(new_detail)
                tr.hops[enum].steps.append(new_step)

        # add to the list of trace results
        rr.trace_result.append(tr)


class TraceResult:
    def __init__(self, traces=None, flow=None) -> None:
        pass

        self.traces = traces
        self.flow = flow


if __name__ == "__main__":
    main()
