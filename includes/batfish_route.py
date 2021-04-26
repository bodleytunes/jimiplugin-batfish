from pybatfish.client.commands import bf_session, bf_init_snapshot, bf_set_network
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints


class batfish_route:
    def __init__(self, src_ip: str, dst_ip: str, dst_port: int) -> None:
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.dst_port = dst_port

    def validate_net(net: any) -> str:

        return net

    def validate_port(port: any) -> int:

        return port