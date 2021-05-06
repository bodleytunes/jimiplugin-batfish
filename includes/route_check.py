from plugins.batfish.includes.batfish import BatFish, BatfishOps


class RouteCheck(BatFish):


    def __init__(self):
        pass


    def check_route(self, start_ip=None, destination_ip=None, snapshot_folder=None):

        b = BatfishOps()
        b.init_batfish(SNAPSHOT_PATH=snapshot_folder)

        print(b.bfq)
        t = b.bfq.traceroute(
            startLocation=start_ip,
            headers=b.hc(
                dstIps=destination_ip
            )
        )
        df = t.answer().frame()

        result = df

        return result

