from typing import Any, Dict, Optional, Union, List


class AcceptResult:
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
        dst_ports: Optional[str] = None,
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
        self.dst_ports = dst_ports
        self.service = service
        self.ip_protocol = ip_protocol
        self.permit_rule = permit_rule
        self.rule_id = rule_id

        self.result_data = result_data


class DeniedResult:
    def __init__(
        self,
        query_node: Optional[str] = None,
        denied: Optional[str] = None,
    ) -> None:
        pass

        self.query_node = query_node
        self.denied = True
