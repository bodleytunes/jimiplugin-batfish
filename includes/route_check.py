from plugins.batfish.includes.batfish import BatFish, BatfishOps


class RouteCheck(BatFish):


    def __init__(self, start_node=None, start_interface=None,  destination_ip=None, snapshot_folder=None):

        self.start_node = start_node
        self.start_interface = start_interface
        self.ingress = f"@enter({start_node}[{start_interface}])"

        pass


    def check(self, ingress=None, destination_ip=None, snapshot_folder=None):

        if ingress is not None:
            self.ingress = ingress
        else:
            ingress == self.ingress


        b = BatfishOps()
        b.init_batfish(SNAPSHOT_PATH=snapshot_folder)

        t = b.bfq.traceroute(
            startLocation=ingress,
            headers=b.hc(
                dstIps=destination_ip
            )
        )
        df = t.answer().frame()

        result = df

        return result

