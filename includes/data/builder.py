from abc import ABC, abstractmethod
from typing import Dict, Tuple, List
import re

from plugins.batfish.includes.result_models.access import AcceptResult, DeniedResult


class DataBuilder(ABC):
    @abstractmethod
    def build_data():
        pass


class AccessDataBuilder(DataBuilder):

    accept_results: list
    denied_results: list

    def __init__(self) -> None:

        self.accept_results = list()
        self.denied_results = list()

    def build_data(self, results_dict: Dict) -> Tuple[List[dict], List[dict]]:

        """Build event data results

        Args:
            results_dict (List[pd.DataFrame]): Pass in list of dataframes (one per node)

        Returns:
            Tuple[List[dict], List[dict]]: 2 Lists of dicts for denied results and accept results
        """

        # Walks its way through a deply nested dataframe type structure
        for node, result in results_dict.items():

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
                            self.accept_results.append(accept_result)

                    else:
                        # generate a DENY entry
                        denied_result = DeniedResult()

                        denied_result.denied = True
                        denied_result.query_node = node

                        self.denied_results.append(denied_result)

        # then whittle all denied results down to only one per query node
        # if we find a node entry in accessresults then remove all from denied
        traffic_denied_hosts = self._remove_denied(
            self.accept_results, self.denied_results
        )
        traffic_denied_hosts = self._remove_dupes(traffic_denied_hosts)

        # empty denied results list
        self.denied_results.clear()
        # create a new unique list of denied results
        for i in traffic_denied_hosts:
            for item in list(i):
                denied_result = DeniedResult()
                denied_result.query_node = item
                denied_result.denied = True
                self.denied_results.append(denied_result)

        # convert the AcceptResult() and DenyResult() objects to dictionaries so they can be consumed by eventData
        self.deny_results = [obj.__dict__ for obj in self.denied_results]
        self.accept_results = [obj.__dict__ for obj in self.accept_results]

        # return deny_results, accept_results
