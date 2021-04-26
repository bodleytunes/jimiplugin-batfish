from pybatfish.client.commands import bf_session, bf_init_snapshot, bf_set_network
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints


class batfish:
    def __init__(self, src_ip, dst_ip, dst_port) -> None:
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.dst_port = dst_port

    def validate_net(net: any) -> str:

        return net

    def validate_port(port: any) -> int:

        return port