import enum
from typing import List
from pandas.errors import EmptyDataError

from plugins.batfish.includes.result_models.traceroute import DataviewTraceroute
from plugins.batfish.includes.batfish import Batfish


class TraceRouteCheck(Batfish):
    def __init__(
        self,
        start_node=None,
        start_interface=None,
        destination_ip=None,
        snapshot_folder=None,
        b_fish=None,
    ):

        self.start_node = start_node
        self.start_interface = start_interface
        if start_interface:
            self.ingress = f"@enter({start_node}[{start_interface}])"
        else:
            self.ingress = f"@enter({start_node})"

        self.b_fish = b_fish

        pass

    def check(
        self,
        ingress=None,
        destination_ip=None,
        snapshot_folder=None,
        start_node=None,
        start_interface=None,
    ):

        self.destination_ip = destination_ip

        if ingress is not None:
            self.ingress = ingress
        else:
            ingress = self.ingress

        result = self.b_fish.bfq.traceroute(
            startLocation=ingress, headers=self.b_fish.hc(dstIps=destination_ip)
        )

        result = result.answer().frame()
        # separate out Flow and Traces
        try:
            # Todo (flow is unused currently)
            flow = result.iloc[0]["Flow"]
        except EmptyDataError as e:
            print(e)
            raise EmptyDataError(f"No data in dataframe location: {e}")
        try:
            traces = result.iloc[0]["Traces"]
        except EmptyDataError as e:
            print(e)
            raise EmptyDataError(f"No data in dataframe location: {e}")

        self.dvt = DataviewTraceroute()

        self._generate_dataview(traces)
        self.dvt_dict = self._generate_dict()

        # finally return data
        return self.dvt_list, self.new_list

    def _generate_dataview(self, traces) -> List[DataviewTraceroute]:

        self.dvt_list = []

        for trace in traces:
            print(f"Trace dispostion: {trace.disposition}")
            # create new dataview traceroute
            dvt = DataviewTraceroute()

            for hop in trace:
                print(f"hop node: {hop.node}")
                dvt.hop_node = hop.node
                for step in hop:
                    if step.action == "ORIGINATED":
                        print(
                            f"step detail originating VRF: {step.detail.originatingVrf}"
                        )
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
            self.dvt_list.append(dvt)

    def _generate_dict(self):

        temp_dict = [obj.__dict__ for obj in self.dvt_list]

        self.new_list = []

        for i, item in enumerate(temp_dict):
            self.new_list.append({f"path{i}": item})
