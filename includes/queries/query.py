from abc import ABC, abstractmethod
import sys
import os
from typing import Any

PACKAGE_PARENT = "../../../../"
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path


from plugins.batfish.includes.batfish import Batfish


class Query(ABC):
    @abstractmethod
    def make_query(
        self,
    ):
        pass


# class QueryType:
#    def __init__(self):
#        pass


class AccessQuery(Query):
    def __init__(self, src_ip, dst_ip):

        self.src_ip = src_ip
        self.dst_ip = dst_ip

    @abstractmethod
    def _create_flow(self):
        # create flow
        pass

    @abstractmethod
    def make_query(self):
        pass


class BatfishQuery:
    nodes: list

    def __init__(self, a: AccessQuery, nodes=None):

        self.b_fish = Batfish(
            host="10.12.12.134",
            snapshot_folder="/shared/data/storage/firewall-configs/snapshot",
        )
        self.nodes = nodes


class PortAccessQuery(AccessQuery):

    src_ip: str
    dst_ip: str
    dst_ports: str

    def __init__(self):
        self.port = None
        self.flow = None
        self.query = None

    def _create_flow(
        self,
    ):
        self.flow = self.b_fish.hc(
            srcIps=self.src_ip,
            dstIps=self.dst_ip,
            dstPorts=self.dst_ports,
        )
        # create flow

        pass

    def make_query(self):

        self.query = self.b_fish.bfq.testFilters(headers=self.flow, nodes=self.nodes)


class ProtocolAccessQuery(AccessQuery):
    def __init__(self, protocol):
        self.protocol = protocol

    def _create_flow(
        self,
    ):
        # create flow
        pass

    def make_query(self):
        self.b_fish.bfq()
        pass

    # def make_query():
