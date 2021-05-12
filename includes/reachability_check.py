from pybatfish.datamodel.flow import PathConstraints
from plugins.batfish.includes.batfish import BatFish, BatfishOps


class ReachabilityCheck(BatFish):
    def __init__(
        self,
        destination_ip=None,
        snapshot_folder=None,
        source_ip=None,
        applications=None,
        dst_ports=None,
        start_location=None,
    ):

        self.srcIps = source_ip
        self.dstIps = destination_ip
        self.applications = applications
        self.dstPorts = dst_ports
        self.start = start_location

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

        b = BatfishOps()
        b.init_batfish(SNAPSHOT_PATH=snapshot_folder)

        t = b.bfq.reachability(
            pathConstraints=b.pc(startLocation=start_location),
            headers=b.hc(
                srcIps=self.srcIps,
                dstIps=self.dstIps,
                applications=self.applications,
                dstPorts=self.dst_ports,
            ),
        )
        df = t.answer().frame()

        result = df

        return result
