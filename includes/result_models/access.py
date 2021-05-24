from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass


@dataclass(order=True)
class AcceptResult:

    query_node: str = None
    flow_result: str = None
    flow_details: Any = None
    trace_tree_list: Any = None
    ingress_egress: str = None
    ingress_zone: str = None
    ingress_interface: str = None
    egress_interface: str = None
    egress_zone: str = None
    ingress_vrf: str = None
    ingress_node: str = None
    source_address: str = None
    destination_address: str = None
    dst_ports: str = None
    dst_ports_list: list = None
    service: str = None
    ip_protocol: str = None
    permit_rule: str = None
    rule_id: str = None

    result_data: Any = None


@dataclass
class DeniedResult:

    query_node: str = None
    denied: bool = None
