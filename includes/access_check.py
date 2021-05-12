from typing import Any, Dict, Optional, Union, List
import re
from plugins.batfish.includes.batfish import Batfish
from collections import defaultdict


class AcceptResult(object):
    def __init__(
        self,
        query_node: Optional[str] = None,
        flow_result: Optional[str] = None,
        flow_details: Optional[str] = None,
        trace_tree_list: Optional[str] = None,
        ingress_egress: Optional[str] = None,
        ingress_zone: Optional[str] = None,
        ingress_interface: Optional[str] = None,
        egress_interface: Optional[str] = None,
        egress_zone: Optional[str] = None,
        ingress_vrf: Optional[str] = None,
        ingress_node: Optional[str] = None,
        source_address: Optional[str] = None,
        destination_address: Optional[str] = None,
        service: Optional[str] = None,
        ip_protocol: Optional[str] = None,
        permit_rule: Optional[str] = None,
        rule_id: Optional[str] = None,
        result_data: Optional[str] = None,
    ) -> None:
        pass

        self.query_node = query_node
        self.flow_result = flow_result
        self.flow_details = flow_details
        self.trace_tree_list = trace_tree_list
        self.ingress_egress = ingress_egress
        self.ingress_zone = ingress_zone
        self.ingress_interface = ingress_interface
        self.egress_interface = egress_interface
        self.egress_zone = egress_zone
        self.ingress_vrf = ingress_vrf
        self.ingress_node = ingress_node
        self.source_address = source_address
        self.destination_address = destination_address
        self.service = service
        self.ip_protocol = ip_protocol
        self.permit_rule = permit_rule
        self.rule_id = rule_id

        self.result_data = result_data


class DeniedResult(object):
    def __init__(
        self,
        query_node: Optional[str] = None,
        denied: Optional[str] = None,
    ) -> None:
        pass

        self.query_node = query_node
        self.denied = True


class AccessCheck(Batfish):
    def __init__(
        self,
        batfish_server: Optional[str] = None,
        host: Optional[str] = None,
        ingress: Optional[str] = None,
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

        # Instance of batfish object
        self.b_fish = b_fish

        pass

    def check(
        self,
        ingress=None,
        src_ip=None,
        destination_ip=None,
        applications=None,
        dst_ports=None,
        ip_protocols=None,
        nodes=None,
        snapshot_folder=None,
    ):

        if applications is not None:

            flow = self.b_fish.hc(
                srcIps=src_ip,
                dstIps=destination_ip,
                applications=self._filter_text(applications),
            )

        elif dst_ports is not None:

            flow = self.b_fish.hc(
                srcIps=src_ip,
                dstIps=destination_ip,
                dstPorts=self._filter_text(dst_ports),
                ipProtocols=self._make_upper(ip_protocols),
            )

        query = self.b_fish.bfq.testFilters(headers=flow, nodes=nodes)

        result = query.answer().frame()

        return result

    def get_results(
        self,
        src_ip=None,
        destination_ip=None,
        applications=None,
        dst_ports=None,
        ip_protocols=None,
        nodes=None,
    ) -> Dict[str, Any]:

        self.src_ip = src_ip
        self.destination_ip = destination_ip
        self.applications = applications
        self.dst_ports = dst_ports
        self.ip_protocols = ip_protocols
        self.nodes = nodes

        results_dict = defaultdict(list)

        for node in self.nodes:

            if self.applications:

                result = self.check(
                    src_ip=self.src_ip,
                    destination_ip=self.destination_ip,
                    applications=self.applications,
                    nodes=node,
                    snapshot_folder=self.snapshot_folder,
                )
            elif self.dst_ports:

                result = self.check(
                    src_ip=self.src_ip,
                    destination_ip=self.destination_ip,
                    dst_ports=self.dst_ports,
                    ip_protocols=self.ip_protocols,
                    nodes=node,
                    snapshot_folder=self.snapshot_folder,
                )

            results_dict[node].append(result)

        merged_results = self._build_access_result(results_dict)

        return merged_results

    def _build_access_result(self, results_dict) -> Union[AcceptResult, DeniedResult]:

        access_results = []
        denied_results = []

        for node, result in results_dict.items():

            for r in result:

                for v in r.values:
                    if re.search("permit", v[3], re.IGNORECASE):
                        access_result = AcceptResult()
                        access_result.query_node = node

                        if len(v[5]) > 0:
                            for item in v[5]:
                                for item_child in item.children:
                                    for c in item_child.children:
                                        if re.search(
                                            "permitted",
                                            c.traceElement.fragments[0].text,
                                            re.IGNORECASE,
                                        ):
                                            for enum, e in enumerate(v):
                                                if enum == 3:
                                                    access_result.flow_result = e
                                                    continue
                                                if enum == 0:
                                                    print(f"Node Queried is: {e}")

                                                if enum == 1:

                                                    access_result.ingress_egress = e

                                                    # split ingress egress string
                                                    (
                                                        ingress_zone,
                                                        ingress_iface,
                                                        egress_zone,
                                                        egress_iface,
                                                    ) = self._split_ingress_egress(
                                                        access_result.ingress_egress
                                                    )
                                                    access_result.ingress_zone = (
                                                        ingress_zone
                                                    )
                                                    access_result.ingress_interface = (
                                                        ingress_iface
                                                    )
                                                    access_result.egress_zone = (
                                                        egress_zone
                                                    )
                                                    access_result.egress_interface = (
                                                        egress_iface
                                                    )
                                                if enum == 2:
                                                    access_result.flow_details = e
                                                    # other details
                                                    access_result.destination_address = (
                                                        access_result.flow_details.dstIp
                                                    )
                                                    access_result.source_address = (
                                                        access_result.flow_details.srcIp
                                                    )
                                                    access_result.service = (
                                                        access_result.flow_details.ipProtocol
                                                    )
                                                    access_result.ingress_node = (
                                                        access_result.flow_details.ingressNode
                                                    )
                                                    access_result.ingress_vrf = (
                                                        access_result.flow_details.ingressVrf
                                                    )
                                                if enum == 4:
                                                    pass
                                                if enum == 5:
                                                    print(f"TraceTreeList: {e}")
                                                    print("========================")
                                                    access_result.trace_tree_list = e
                                                    # get policy permit details / rule details
                                                    access_result.permit_rule = (
                                                        access_result.trace_tree_list[0]
                                                        .traceElement.fragments[1]
                                                        .text
                                                    )
                                                    access_result.rule_id = (
                                                        access_result.trace_tree_list[0]
                                                        .traceElement.fragments[2]
                                                        .text
                                                    )

                        if access_result.flow_result == "PERMIT":
                            access_results.append(access_result)

                    else:
                        # generate a DENY entry

                        denied_result = DeniedResult()

                        denied_result.denied == True
                        denied_result.query_node = node

                        denied_results.append(denied_result)

        merged_results = [*access_results, *denied_results]

        # todo
        permit_results = [obj.__dict__ for obj in access_results]
        deny_results = [obj.__dict__ for obj in denied_results]

        return permit_results, deny_results, merged_results

    def _split_ingress_egress(self, ingress_egress):

        split_list = ingress_egress.split("~")

        ingress_zone = split_list[0]
        ingress_iface = split_list[1]
        egress_zone = split_list[3]
        egress_iface = split_list[4]

        return ingress_zone, ingress_iface, egress_zone, egress_iface

    def _filter_text(self, arg):
        # filter empty "" or ''
        if arg:
            converter = lambda i: i or None
            result = [converter(i) for i in arg]
            return result
        return

    def _make_upper(self, arg):
        #  make protocols uppercase
        if arg:
            result = [x.upper() for x in arg]
            return result
        return
