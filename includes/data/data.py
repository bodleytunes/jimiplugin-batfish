from abc import ABC, abstractmethod
import sys
import os
from typing import Any, DefaultDict, List, Tuple
import re
from logging import exception

PACKAGE_PARENT = "../../../../"
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path


from plugins.batfish.includes.batfish import Batfish
from plugins.batfish.includes.bat_helpers import BatHelpers
from plugins.batfish.includes.result_models.access import AcceptResult, DeniedResult
from plugins.batfish.includes.queries.access_check import AccessCheck


class Walkable(AccessCheck, ABC):
    @abstractmethod
    def walk_data(
        self,
    ):
        pass


class DataWalker(Walkable):
    def __init__(self, src_ip, dst_ip, results_dict: DefaultDict[str, List[Any]]):

        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.results_dict = results_dict

    @abstractmethod
    def walk_data(self):
        # create flow
        pass


class AccessCheckDataWalker(DataWalker):
    nodes: list

    src_ip: str
    dst_ip: str
    dst_ports: str

    def __init__(self):
        self.port = None
        self.flow = None
        self.query = None

    def walk_data(
        self,
    ):
        accept_results = list()
        denied_results = list()

        # Walks its way through a deply nested dataframe type structure
        for node, result in self.results_dict.items():

            for r in result:

                for v in r.values:
                    # if re: hits a "permit" then do something
                    if re.search("permit", v[3], re.IGNORECASE):
                        accept_result = AcceptResult()
                        accept_result.query_node = node

                        if len(v[5]) > 0:
                            for item in v[5]:
                                for item_child in item.children:
                                    for c in item_child.children:
                                        # if re: hits a "permitted" then dig deeper
                                        if re.search(
                                            "permitted",
                                            c.traceElement.fragments[0].text,
                                            re.IGNORECASE,
                                        ):
                                            for enum, e in enumerate(v):
                                                if enum == 3:
                                                    accept_result.flow_result = e
                                                    continue
                                                if enum == 0:
                                                    print(f"Node Queried is: {e}")

                                                if enum == 1:
                                                    # start adding data to the AcceptResult() objects fields
                                                    accept_result.ingress_egress = e

                                                    # split ingress/egress string into separate fields/attributes
                                                    (
                                                        ingress_zone,
                                                        ingress_iface,
                                                        egress_zone,
                                                        egress_iface,
                                                    ) = self._split_ingress_egress(
                                                        accept_result.ingress_egress
                                                    )
                                                    accept_result.ingress_zone = (
                                                        ingress_zone
                                                    )
                                                    accept_result.ingress_interface = (
                                                        ingress_iface
                                                    )
                                                    accept_result.egress_zone = (
                                                        egress_zone
                                                    )
                                                    accept_result.egress_interface = (
                                                        egress_iface
                                                    )
                                                if enum == 2:

                                                    accept_result.flow_details = e

                                                    # Add details relating to IP headers/5 tuple
                                                    accept_result.destination_address = (
                                                        accept_result.flow_details.dstIp
                                                    )
                                                    accept_result.source_address = (
                                                        accept_result.flow_details.srcIp
                                                    )
                                                    accept_result.dst_ports = (
                                                        accept_result.flow_details.dstPort
                                                    )
                                                    accept_result.service = (
                                                        accept_result.flow_details.ipProtocol
                                                    )
                                                    accept_result.ingress_node = (
                                                        accept_result.flow_details.ingressNode
                                                    )
                                                    accept_result.ingress_vrf = (
                                                        accept_result.flow_details.ingressVrf
                                                    )

                                                    # Now resetting this to None as it would add a nested object of type Flow()
                                                    accept_result.flow_details = None

                                                if enum == 4:
                                                    pass
                                                if enum == 5:
                                                    accept_result.trace_tree_list = e
                                                    # get policy permit details / rule details
                                                    accept_result.permit_rule = (
                                                        accept_result.trace_tree_list[0]
                                                        .traceElement.fragments[1]
                                                        .text
                                                    )
                                                    accept_result.rule_id = (
                                                        accept_result.trace_tree_list[0]
                                                        .traceElement.fragments[2]
                                                        .text
                                                    )
                                                    # resetting this to None as it would add a nested object of type TraceTreeList
                                                    accept_result.trace_tree_list = None

                        if accept_result.flow_result == "PERMIT":
                            accept_results.append(accept_result)

                    else:
                        # generate a DENY entry
                        denied_result = DeniedResult(denied=True, query_node=node)

                        denied_results.append(denied_result)

        # split data delimited by ~ into separate strings

    def _split_ingress_egress(self, ingress_egress: str) -> Tuple[str, str, str, str]:

        split_list = ingress_egress.split("~")

        ingress_zone = split_list[0]
        ingress_iface = split_list[1]
        egress_zone = split_list[3]
        egress_iface = split_list[4]

        return ingress_zone, ingress_iface, egress_zone, egress_iface

    # remove any deny results if a node has an accept
    def _remove_denied(self, accept_results, denied_results) -> List[DeniedResult]:
        # remove denied entries
        for a in accept_results:
            # iterate over copy as don't delete from list while iterating
            for d in list(denied_results):
                if d.query_node == a.query_node:
                    # remove this denied entry
                    denied_results.remove(d)

        return denied_results

    # remove duplicate hits
    def _remove_dupes(self, denied_results) -> list:

        # make unique/remove repeated denies/duplicate nodes
        denied_hosts_list = [d.query_node for d in denied_results]
        unique_denied_hosts_list = set(denied_hosts_list)
        # to list
        traffic_denied_hosts = [unique_denied_hosts_list]

        return traffic_denied_hosts


class PreFlight(ABC):
    @abstractmethod
    def run_pre_flight_checks(self):
        pass


class DataWalkerPreflight:
    def __init__(self, p: PreFlight):
        # shared vars go here
        self.src_ip
        self.dst_ip


class AccessCheckPreFlight(PreFlight):
    def __init__(self) -> None:
        pass

    def run_pre_flight_checks(self):

        # validate IP's
        if self.src_ip:
            self.src_ip = BatHelpers.check_valid_ip(self.src_ip)
        if self.dst_ip:
            self.dst_ip = BatHelpers.check_valid_ip(self.dst_ip)
        # validate ports
        # validate protocols
        # validate apps

        # sanity check source and destination exist
        if not self.src_ip and not self.dst_ip:
            raise exception("Need to have at least a source or dest IP")
        # empty source/dest changed to 0.0.0.0/0
        if not self.src_ip:
            self.src_ip = "0.0.0.0/0"
        if not self.dst_ip:
            self.dst_ip = "0.0.0.0/0"
