from plugins.batfish.includes.batfish import Batfish


class IpOwners(Batfish):
    def __init__(self):
        pass

    def get_ip_owners(self, snapshot_folder=None):

        b = Batfish()
        b.init_batfish(SNAPSHOT_PATH=snapshot_folder)

        r = b.bfq.ipOwners()

        df = r.answer().frame()

        result = df

        return result
