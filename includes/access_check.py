from plugins.batfish.includes.batfish import BatFish, BatfishOps


class AccessCheck(BatFish):


    def __init__(self, ingress=None, src_ip=None, destination_ip=None, applications=None, nodes=None, snapshot_folder=None):

        self.src_ip = src_ip
        self.destination_ip = destination_ip
        self.applications = applications
        self.snapshot_folder = snapshot_folder
        self.nodes = "hub2"

        pass


    def check(self, ingress=None, src_ip=None, destination_ip=None, applications=None, nodes=None, snapshot_folder=None):



        b = BatfishOps()
        b.init_batfish(SNAPSHOT_PATH=snapshot_folder)

        
        flow = b.hc(srcIps=src_ip,
                     dstIps=destination_ip,
                     applications=applications)

        t = b.bfq.testFilters(headers=flow,
                         nodes=nodes)

        


        df = t.answer().frame()

        result = df

        return result

