from dataclasses import dataclass


@dataclass()
class DataviewTraceroute:

    trace_disposition: str = None
    hop_node: str = None
    originatin_vrf: str = None
    arp_ip: str = None
    next_hop_ip: str = None
    resolved_next_hop_ip: str = None
    output_interface: str = None
    network: str = None
    via_protocol: str = None
