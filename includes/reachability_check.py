from plugins.batfish.includes.batfish import Batfish


class ReachabilityCheck(Batfish):
    def __init__(
        self,
        destination_ip=None,
        snapshot_folder=None,
        source_ip=None,
        applications=None,
        dst_ports=None,
        start_location=None,
        b_fish=None,
    ):

        self.srcIps = source_ip
        self.dstIps = destination_ip
        self.applications = applications
        self.dstPorts = dst_ports
        self.start = start_location

        self.b_fish = b_fish

        pass

    def check(
        self,
        ingress=None,
        destination_ip=None,
        snapshot_folder=None,
        srcIps=None,
        dstIps=None,
        applications=None,
        dst_ports=None,
        start_location=None,
    ):

        t = self.b_fish.bfq.reachability(
            pathConstraints=self.b_fish.pc(startLocation=start_location),
            headers=self.b_fish.hc(
                srcIps=self.srcIps,
                dstIps=self.dstIps,
                applications=self.applications,
                dstPorts=self.dst_ports,
            ),
        )
        result = t.answer().frame()

        return result
