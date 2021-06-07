from typing import Any, Dict


import json

from plugins.batfish.includes.batfish import Batfish
from plugins.batfish.includes.result_models.reachability import (
    TraceResult,
    ReachabilityResult,
    FlowResult,
    Step,
    Hop,
    Detail,
    Route,
    Flow,
)


class ReachabilityCheck(Batfish):
    def __init__(
        self,
        destination_ip=None,
        snapshot_folder=None,
        source_ip=None,
        applications=None,
        dst_ports=None,
        start_node=None,
        start_interface=None,
        b_fish=None,
    ):

        self.srcIps = source_ip
        self.dstIps = destination_ip
        self.applications = applications
        self.dstPorts = dst_ports
        self.start = start_node
        self.start_interface = start_interface

        self.rr = ReachabilityResult()
        self.tr = TraceResult()
        self.fl = FlowResult()



        self.trace_result: dict

        self.b_fish = b_fish

        pass

    def check(
        self,
        **kwargs: Dict[Any, Any],
    ) -> ReachabilityResult:

        # unpack keyword args
        for key, value in kwargs.items():
            setattr(self, key, value)

        result = self.b_fish.bfq.reachability(
            pathConstraints=self.b_fish.pc(startLocation=self.start),
            headers=self.b_fish.hc(
                srcIps=self.srcIps,
                dstIps=self.dstIps,
                applications=self.applications,
                dstPorts=self.dstPorts,
            ),
        )

        result = result.answer().frame()

        # separate out Flow and Traces
        try:
            flow = result.iloc[0]["Flow"]


        except BaseException as e:
            raise BaseException(f"out of bounds {e}")

        try:
            traces = result.iloc[0]["Traces"]
        except BaseException as e:
            raise BaseException(f"out of bounds {e}")

        self.rr = ReachabilityResult()

        self._generate_flow_data(flow)
        self._generate_trace_data(traces)

        self.rr.flow_result = self.fl

        # return RR as event data back to jimi flow
        return self.rr

    def _generate_flow_data(self, flow) -> FlowResult:

        self.fl = FlowResult()

        self.fl.src_ip = flow.srcIp
        self.fl.dst_ip = flow.dstIp
        self.fl.ip_protocol = flow.ipProtocol




        self.fl.destination_ingress_node = flow.ingressNode
        self.fl.ingress_vrf = flow.ingressVrf

    def _generate_trace_data(self, traces) -> TraceResult:

        for trace in traces:
            self.tr = TraceResult()
            self.tr.trace_disposition = trace.disposition

            for hop in trace:

                self.tr.hops = []
                new_hop = Hop()

                for step in hop:
                    new_step = Step()

                    if step.action == "ORIGINATED":

                        new_step.action = "ORIGINATED"

                        new_detail = Detail()
                        # add to detail
                        new_detail.originating_vrf = step.detail.originatingVrf

                        new_step.details.append(new_detail)

                    elif step.action == "FORWARDED":

                        new_step.action = "FORWARDED"
                        new_detail = Detail()

                        new_detail.arp_ip = step.detail.arpIp
                        new_detail.output_interface = step.detail.outputInterface

                        for route in step.detail.routes:
                            new_route = Route()

                            # Put assertions in here?
                            new_route.network = route["network"]
                            new_route.next_Hop = route["nextHopIp"]
                            new_route.via_protocol = route["protocol"]

                            new_detail.routes.append(new_route)

                        new_step.details.append(new_detail)

                    elif step.action == "PERMITTED":

                        new_step.action = "PERMITTED"

                        new_detail = Detail()
                        new_flow = Flow()

                        new_detail.filter = step.detail.filter
                        new_detail.filter_type = step.detail.filterType

                        new_flow.dst_ip = step.detail.flow.dstIp
                        new_flow.dst_port = step.detail.flow.dstPort
                        new_flow.ingress_node = step.detail.flow.ingressNode
                        new_flow.ingress_interface = step.detail.flow.ingressInterface
                        new_flow.ingress_vrf = step.detail.flow.ingressVrf
                        new_flow.ip_protocol = step.detail.flow.ipProtocol
                        new_flow.src_ip = step.detail.flow.srcIp

                        new_detail.flow = new_flow
                        new_step.details.append(new_detail)

                    elif step.action == "TRANSMITTED":

                        new_step.action = "TRANSMITTED"

                        new_detail = Detail()

                        new_detail.output_interface = step.detail.outputInterface

                        new_step.details.append(new_detail)

                    elif step.action == "EXITS_NETWORK":

                        new_step.action = "EXITS_NETWORK"
                        new_detail = Detail()

                        new_detail.output_interface = step.detail.outputInterface
                        new_detail.resolve_next_hop = step.detail.resolvedNexthopIp

                        new_step.details.append(new_detail)

                    # append steps to hop
                    new_hop.steps.append(new_step)

                # add new hop to traceroute
                self.tr.hops.append(new_hop)

            # finally append trace to reachability result
            self.rr.trace_result.append(self.tr)



            # return a dictionary of the nested objects to be consumed by jimi
            self.trace_result: dict = self._build_dict(self.rr)

    # build a dictionary from the nested objects using a lambda/anonymous function
    def _build_dict(self, obj):
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__))
