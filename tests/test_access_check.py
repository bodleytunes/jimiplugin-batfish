# Fudge the python path
import sys
import os
from typing import Any, Dict, Optional, Union, List
from collections import defaultdict

import pandas as pd
import pytest
import re


PACKAGE_PARENT = "../../../"
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.access_check import AccessCheck


# INPUT FIELDS

# IP's
src_ip = "10.1.255.100"
destination_ip = "10.3.255.100"

# Services
# applications =["dns"]
applications = ["icmp"]
# applications = ["https"]

# Nodes to query
nodes = "spoke1"
node_list = ["spoke1", "spoke2"]

# OUTPUT OBJECTS
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


@pytest.mark.batfish
def main():

    ac = AccessCheck()

    results = ac.check(
        src_ip=src_ip,
        destination_ip=destination_ip,
        applications=applications,
        nodes=nodes,
        snapshot_folder="/shared/data/storage/firewall-configs/snapshot",
    )

    all_results = []

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)

    result_dict = _build_results_dict(ac)

    # build new access_result object
    access_results = _build_access_result(result_dict)
    print(access_results)


def _build_results_dict(ac) -> Dict[str, Any]:

    results_dict = defaultdict(list)

    for node in node_list:
        result = ac.check(
            src_ip=src_ip,
            destination_ip=destination_ip,
            applications=applications,
            nodes=node,
            snapshot_folder="/shared/data/storage/firewall-configs/snapshot",
        )
        results_dict[node].append(result)

    return results_dict


def _build_access_result(results_dict) -> Union[AcceptResult, DeniedResult]:

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
                                                print("========================")
                                                print(f"Flow result : *** {e} ***")
                                                access_result.flow_result = e
                                                continue
                                            if enum == 0:
                                                print(f"Node Queried is: {e}")

                                            if enum == 1:
                                                print(
                                                    f"From zone/iface to zone/iface: {e}"
                                                )
                                                access_result.ingress_egress = e

                                                # split ingress egress string
                                                (
                                                    ingress_zone,
                                                    ingress_iface,
                                                    egress_zone,
                                                    egress_iface,
                                                ) = _split_ingress_egress(
                                                    access_result.ingress_egress
                                                )
                                                access_result.ingress_zone = (
                                                    ingress_zone
                                                )
                                                access_result.ingress_interface = (
                                                    ingress_iface
                                                )
                                                access_result.egress_zone = egress_zone
                                                access_result.egress_interface = (
                                                    egress_iface
                                                )
                                            if enum == 2:
                                                print(f"Flow details: {e}")
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

    return merged_results


def _split_ingress_egress(ingress_egress):

    split_list = ingress_egress.split("~")

    ingress_zone = split_list[0]
    ingress_iface = split_list[1]
    egress_zone = split_list[3]
    egress_iface = split_list[4]

    return ingress_zone, ingress_iface, egress_zone, egress_iface


if __name__ == "__main__":
    main()
