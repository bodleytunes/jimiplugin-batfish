# Fudge the python path
import sys
import os
from typing import Any, Dict, Optional, Union, List
from collections import defaultdict
import pprint

import pandas as pd
import pytest
import re


PACKAGE_PARENT = "../../../"
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.queries.access_check import AccessCheck
from plugins.batfish.includes.batfish import Batfish


# INPUT FIELDS

# IP's
src_ip = "10.1.255.100"
destination_ip = "172.16.4.2"

# Services
# applications =["dns"]
applications = ["icmp"]
# applications = ["https"]
# dst_ports = ["80"]
dst_ports = None

# Nodes to query
# nodes = ["spoke1"]
nodes = ["spoke1", "spoke2", "hub2", "sat1", "sat2", "sat3", "the-internet"]

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

    """
    * Initialize AccessCheck Object from access_check.py
    * run _build_results_dict and pass in AccessCheck() object as arg
    * inits batfish() object
    * creates flow from passed in args
    * Batfish make a Query "testFilters" and pass in "flow" and "nodes" as args
    * returns resulting answer as a dataframe
    """

    b_fish = Batfish(
        host="10.12.12.134",
        snapshot_folder="/shared/data/storage/firewall-configs/snapshot",
    )

    ac = AccessCheck(b_fish=b_fish)

    permit_results, deny_results, accept_results, results = ac.get_results(
        src_ip=src_ip,
        destination_ip=destination_ip,
        applications=applications,
        dst_ports=dst_ports,
        nodes=nodes,
    )

    # print(results)
    # get a dict from each of the objects
    # accept_results = [accept_result.__dict__ for accept_result in accept_results]
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(accept_results)


if __name__ == "__main__":
    main()
