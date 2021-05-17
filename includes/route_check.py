from typing import Dict, Any
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
from plugins.batfish.includes.helpers import *


class RouteCheck(Batfish):
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
        self.ingress = f"@enter({start_node}[{start_interface}])"

        self.b_fish = b_fish

        pass

    def check(
        self,
        **kwargs: Dict[Any, Any],
    ):

        # unpack keyword args
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.ingress = f"@enter({self.start_node}[{self.start_interface}])"

        results = self.b_fish.bfq.traceroute(
            startLocation=self.ingress,
            headers=self.b_fish.hc(dstIps=self.destination_ip),
        )
        #! todo fix this
        flow = results["Flow"]
        results = results["Traces"]

        self.fl = FlowResult()
        self.fl.generate_flow_data()

        # results = t.answer().frame()

        return flow
