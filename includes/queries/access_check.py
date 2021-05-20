from typing import Optional, List, Tuple
import re
from collections import defaultdict

import pandas as pd


from plugins.batfish.includes.batfish import Batfish
from plugins.batfish.includes.result_models.access import AcceptResult, DeniedResult
from pybatfish.exception import BatfishException


class AccessCheck(Batfish):
    def __init__(
        self,
        batfish_server: Optional[str] = None,
        host: Optional[str] = None,
        src_ip: Optional[str] = None,
        destination_ip: Optional[str] = None,
        applications: Optional[str] = None,
        dst_ports: Optional[str] = None,
        ip_protocols: Optional[list] = None,
        nodes: Optional[str] = None,
        snapshot_folder: Optional[str] = None,
        b_fish=None,
    ):

        self.batfish_server = batfish_server
        self.host = host
        self.src_ip = src_ip
        self.destination_ip = destination_ip
        self.applications = applications
        self.dst_ports = dst_ports
        self.ip_protocols = ip_protocols
        self.snapshot_folder = snapshot_folder
        self.nodes = "hub2"

        # Instance of a batfish object
        self.b_fish = b_fish

        pass

    def get_results(
        self,
        src_ip=None,
        destination_ip=None,
        applications=None,
        dst_ports=None,
        ip_protocols=None,
        nodes=None,
    ) -> Tuple[List[dict], List[dict]]:
        """Get Batfish Results

        Args:
            src_ip (string, optional): source ip. Defaults to None.
            destination_ip (string, optional): destination ip. Defaults to None.
            applications (list, optional): list of applications. Defaults to None.
            dst_ports (list, optional): list of destination ports. Defaults to None.
            ip_protocols (list, optional): list of protocols. Defaults to None.
            nodes (list, optional): list of nodes(network devices/firewalls etc)to query. Defaults to None.

        Returns:
            Tuple[List[dict], List[dict]]: 2 variables, each a list of dictionaries for permitted and denied results
        """

        self.src_ip = src_ip
        self.destination_ip = destination_ip
        self.applications = applications
        self.dst_ports = dst_ports
        self.ip_protocols = ip_protocols
        self.nodes = nodes

        # create empty list for returned results (Accept and Deny results)
        results_dict = defaultdict(list)

        # Loop through all passed in nodes(Network devices/Firewalls)
        for node in self.nodes:

            # Run access checker function to make the batfish query on a per node basis and return a result for each of them
            result = self._query(nodes=node)

            # Append each nodes query result to the list
            results_dict[node].append(result)

        # process results (walk dataframe) and return dictionary type data suitable for merging with eventData
        (
            deny_results,
            accept_results,
        ) = self._build_results(results_dict)

        # return both deny and results variables to "action"
        return deny_results, accept_results

    def _query(self, nodes=None) -> pd.DataFrame:
        """Do Batfish Query

        Args:
            nodes (list, optional): list of nodes to query. Defaults to None.

        Raises:
            BatfishException: batfish exception

        Returns:
            pd.DataFrame: returns nested structured data frame
        """
        if self.applications is not None:

            # flow is a headerConstraint object which was built from passing in args relating to the source/dst ip/proto (5 tuple etc)
            flow = self.b_fish.hc(
                srcIps=self.src_ip,
                dstIps=self.destination_ip,
                applications=self._filter_text(self.applications),
            )

        elif self.dst_ports is not None:
            # flow is a headerConstraint object which was built from passing in args relating to the source/dst ip/proto (5 tuple etc)
            flow = self.b_fish.hc(
                srcIps=self.src_ip,
                dstIps=self.destination_ip,
                dstPorts=self._filter_text(self.dst_ports),
                ipProtocols=self._make_upper(self.ip_protocols),
            )
        """
        make query
        """
        # nodes is actually a single node here, not sure why batfish have named it "nodes"?
        # flow is a headerConstraint object which was built from passing in args relating to the source/dst ip/proto (5 tuple etc)
        try:
            query = self.b_fish.bfq.testFilters(headers=flow, nodes=nodes)
            result = query.answer().frame()
            return result
        except BatfishException as e:
            print(e)
            raise BatfishException(f"Batfish Query failure :  {e}")
            # return {}

    def _build_results(
        self, results_dict: List[pd.DataFrame]
    ) -> Tuple[List[dict], List[dict]]:
        """Build event data results

        Args:
            results_dict (List[pd.DataFrame]): Pass in list of dataframes (one per node)

        Returns:
            Tuple[List[dict], List[dict]]: 2 Lists of dicts for denied results and accept results
        """

        accept_results = list()
        denied_results = list()

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
                            accept_results.append(accept_result)

                    else:
                        # generate a DENY entry
                        denied_result = DeniedResult()

                        denied_result.denied = True
                        denied_result.query_node = node

                        denied_results.append(denied_result)

        # then whittle all denied results down to only one per query node
        # if we find a node entry in accessresults then remove all from denied
        traffic_denied_hosts = self._remove_denied(accept_results, denied_results)
        traffic_denied_hosts = self._remove_dupes(traffic_denied_hosts)

        # empty denied results list
        denied_results.clear()
        # create a new unique list of denied results
        for i in traffic_denied_hosts:
            for item in list(i):
                denied_result = DeniedResult()
                denied_result.query_node = item
                denied_result.denied = True
                denied_results.append(denied_result)

        # convert the AcceptResult() and DenyResult() objects to dictionaries so they can be consumed by eventData
        deny_results = [obj.__dict__ for obj in denied_results]
        accept_results = [obj.__dict__ for obj in accept_results]

        return deny_results, accept_results

    # split data delimited by ~ into separate strings
    def _split_ingress_egress(self, ingress_egress):

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

    def _filter_text(self, arg) -> str:
        # filter empty "" or ''
        if arg:

            def converter(i):
                return i or None

            result = [converter(i) for i in arg]
            return result
        return

    def _make_upper(self, arg) -> str:
        #  make uppercase
        if arg:
            result = [x.upper() for x in arg]
            return result
        return
