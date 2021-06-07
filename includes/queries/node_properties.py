from plugins.batfish.includes.batfish import Batfish


class NodeProperties(Batfish):
    def __init__(self):
        pass

    def check_node_properties(self, snapshot_folder=None):

        b = Batfish()
        b.init_batfish(SNAPSHOT_PATH=snapshot_folder)

        # print(b.bfq)
        r = b.bfq.nodeProperties()

        df = r.answer().frame()

        result = df

        return result




####################################################


from logging import exception
from typing import Optional, List, Tuple, DefaultDict, Any
from collections import defaultdict

import pandas as pd

from pybatfish.exception import BatfishException

from plugins.batfish.includes.batfish import Batfish
from plugins.batfish.includes.bat_helpers import BatHelpers
from plugins.batfish.includes.data.builder import AccessDataBuilder


class NodePropertiesCheck(Batfish):
    def __init__(
        self,
        batfish_server: Optional[str] = None,
        host: Optional[str] = None,
        src_ip: Optional[str] = None,
        dst_ip: Optional[str] = None,
        applications: Optional[list] = None,
        dst_ports: Optional[str] = None,
        ip_protocols: List[Any] = None,
        nodes: Optional[str] = None,
        node: str = None,
        snapshot_folder: Optional[str] = None,
        b_fish=None,
    ):

        self.batfish_server = batfish_server
        self.host = host
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.applications = applications
        self.dst_ports = dst_ports
        self.ip_protocols = ip_protocols
        self.snapshot_folder = snapshot_folder
        # self.nodes = "hub2"

        # Instance of a batfish object
        self.b_fish = b_fish

        pass

    def run(
        self,
        node: Optional[str] = None,
    ):

        # create empty list for returned results (Accept and Deny results)
        self.results_dict: dict = defaultdict(list)

        results = self._query(node)

        self._build_results(results)

        return results

    def _query(self, nodes: Optional[list] = None) -> pd.DataFrame:

        self._make_query(nodes)

    def _make_query(self, nodes):
        """
        make query
        """
        # nodes is actually a single node here, not sure why batfish have named it "nodes"?
        try:
            query = self.b_fish.bfq.nodeProperties(nodes=nodes)
            result = query.answer().frame()
            # Append each nodes query result to the results_dict list
            self.results_dict[nodes].append(result)

        except BatfishException as e:
            print(e)
            raise BatfishException(f"Batfish Query failure :  {e}")

    def _build_results(
        self, results_dict: DefaultDict[str, List[Any]]
    ) -> Tuple[List[dict], List[dict]]:

    

