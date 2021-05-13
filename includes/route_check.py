from plugins.batfish.includes.batfish import Batfish


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

    def check(self, ingress=None, destination_ip=None, snapshot_folder=None):

        self.destination_ip = destination_ip

        if ingress is not None:
            self.ingress = ingress
        else:
            ingress == self.ingress

        t = self.b_fish.bfq.traceroute(
            startLocation=ingress, headers=self.b_fish.hc(dstIps=destination_ip)
        )
        result = t.answer().frame()

        return result
