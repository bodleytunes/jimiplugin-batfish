from plugins.batfish.includes.batfish import BatFish, BatfishOps


class AccessCheck(BatFish):


    def __init__(self, start_node=None, start_interface=None,  destination_ip=None, snapshot_folder=None):

        self.start_node = start_node
        self.start_interface = start_interface
        self.ingress = f"@enter({start_node}[{start_interface}])"

        pass


    def check(self, ingress=None, src_ip=None, destination_ip=None, snapshot_folder=None):



        b = BatfishOps()
        b.init_batfish(SNAPSHOT_PATH=snapshot_folder)

        
        flow = b.hc(srcIps="10.10.10.1",
                     dstIps="218.8.104.58",
                     applications=["dns"])

        t = b.bfq.testFilters(headers=flow,
                         nodes="hub1",
                         filters="acl_in")

        


        df = t.answer().frame()

        result = df

        return result

