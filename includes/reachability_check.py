from pybatfish.datamodel.flow import PathConstraints
from plugins.batfish.includes.batfish import BatFish, BatfishOps


class ReachabilityCheck(BatFish):


    def __init__(self, start_node=None, start_interface=None,  destination_ip=None, snapshot_folder=None, source_ip=None, applications=None, start_location=None):

        self.start_node = start_node
        self.start_interface = start_interface
        self.ingress = f"@enter({start_node}[{start_interface}])"
        self.srcIps = source_ip
        self.dstIps = destination_ip
        self.applications = applications
        self.start = start_location

        pass


    def check(self, ingress=None, destination_ip=None, snapshot_folder=None, srcIps=None, dstIps=None, applications=None, start_location=None):

        

        b = BatfishOps()
        b.init_batfish(SNAPSHOT_PATH=snapshot_folder)

        t = b.bfq.reachability(
            pathConstraints=b.pc(startLocation=start_location),
            headers=b.hc(
                srcIps=self.srcIps, dstIps=self.dstIps, applications=self.applications
            )
        )
        df = t.answer().frame()

        result = df

        return result

