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

    def generate_flow_data(self, flow):

        self.fl.src_ip = flow.srcIp
        self.fl.dst_ip = flow.dstIp
        self.fl.ip_protocol = flow.ipProtocol
        self.fl.destination_ingress_node = flow.ingressNode
        self.fl.ingress_vrf = flow.ingressVrf


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


        self.destination_ingress_node: str
        self.ingress_interface: str
        self.ingress_vrf: str
        self.ip_protocol: str

        pass




# @dataclass
# class ReachabilityResultDataView:
