from plugins.batfish.includes.batfish import BatFish, BatfishOps


class IpOwners(BatFish):


    def __init__(self):
        pass


    def get_ip_owners(self, snapshot_folder=None):

        b = BatfishOps()
        b.init_batfish(SNAPSHOT_PATH=snapshot_folder)

        r = b.bfq.ipOwners()
        
        df = r.answer().frame()

        result = df

        return result

