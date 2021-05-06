from plugins.batfish.includes.batfish import BatFish, BatfishOps


class NodeProperties(BatFish):


    def __init__(self):
        pass


    def check_node_properties(self, snapshot_folder=None):

        b = BatfishOps()
        b.init_batfish(SNAPSHOT_PATH=snapshot_folder)

        #print(b.bfq)
        r = b.bfq.nodeProperties()
        
        df = r.answer().frame()

        result = df

        return result

