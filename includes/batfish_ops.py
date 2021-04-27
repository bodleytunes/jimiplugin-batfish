from pybatfish.client.commands import bf_session, bf_init_snapshot, bf_set_network
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.datamodel.flow import HeaderConstraints


class BatfishOps:
    def __init__(
        self, NETWORK_NAME=None, BATFISH_SERVER=None, SNAPSHOT_PATH=None
    ) -> None:
        self.NETWORK_NAME = "Firewalls"
        self.BATFISH_SERVER = "10.12.12.134"
        self.SNAPSHOT_PATH = SNAPSHOT_PATH

        self.init_batfish()

    def init_batfish(self):

        bf_session.host = self.BATFISH_SERVER
        bf_session.coordinatorHost = self.BATFISH_SERVER

        bf_set_network(self.NETWORK_NAME)

        # Initialize Batfish Snapshot
        bf_init_snapshot(self.SNAPSHOT_PATH, name=self.NETWORK_NAME, overwrite=True)

        # Load Batfish Questions
        load_questions()

    def question_routing(self, src_ip, dst_ip, dst_port=None, applications=None):

        # Get a list of all the nodes/devices
        node_list = self.get_all_devices()

        dst_port_list = list([dst_port])

        if applications is not None:
            # todo - enter application as args
            print("hello world")

        elif dst_port is not None:
            # todo - lookup startLocation based on ip address matching to node

            # todo - enter ports as args
            # traceroute_spoke1 = (
            #    bfq.traceroute(
            #        startLocation="fortigate-vm64-kvm__configs__spoke1.cfg",
            #        headers=HeaderConstraints(dstIps=dst_ip, dstPorts=dst_port_list),
            #    )
            #    .answer()
            #    .frame()
            # )

            traceroutes = []

            for device in node_list:

                traceroute = (
                    bfq.traceroute(
                        startLocation=device,
                        headers=HeaderConstraints(
                            dstIps=dst_ip, dstPorts=dst_port_list
                        ),
                    )
                    .answer()
                    .frame()
                )
                traceroutes.append(traceroute)

        # traces = traceroutes.Traces.iloc

        for t in traceroutes:
            print("================================================================")
            # Destination Network

            # Source device
            # print(f"Traffic sourced from:  {t.Traces.iloc[0].hops[0].node}")
            print(f"Traffic sourced from:  {t.Traces.values[0][0].hops[0].node}")
            # Egress interface
            # print(
            #    f"Next-hop (Egress) interface: {t.Traces.iloc[0].hops[0].steps[3].detail}"
            # )
            print(
                f"Next-hop (Egress) interface: {t.Traces.values[0][0].hops[0].steps[3].detail}"
            )
            # Loop through egress ifaces
            for hop in t.Traces.values[0]:
                print(hop.hops[0].steps[3].detail)
            # Next-hop interface
            # print(
            #    f"Next-hop IP:  {t.Traces.iloc[0].hops[0].steps[1].detail.routes[0]['nextHopIp']}"
            # )
            # Print ECMP next-hop #1
            print(
                f"Next-hop IP:  {t.Traces.values[0][0].hops[0].steps[1].detail.routes[0]['nextHopIp']}"
            )
            # Print ECMP next-hop #2
            print(
                f"Next-hop IP:  {t.Traces.values[0][1].hops[0].steps[1].detail.routes[0]['nextHopIp']}"
            )
            # Loop through ECMP hops
            for hop in t.Traces.values[0]:
                print(hop.hops[0].steps[1].detail.routes[0]["nextHopIp"])

            # Next-hop protocol
            print(
                f"Protocol/route type: {t.Traces.values[0][0].hops[0].steps[1].detail.routes[0]['protocol']}"
            )
            # Loop through protocols
            for hop in t.Traces.values[0]:
                print(
                    f"Protocol/route type: {hop.hops[0].steps[1].detail.routes[0]['protocol']}"
                )

            print("================================================================")
            # Is Permitted

        answer = traceroutes

        return answer

    def get_all_devices(self) -> list:
        nodes = bfq.nodeProperties().answer().frame()

        node_list = []
        # Get Node Strings
        for node in nodes["Node"].iloc:
            print(node)
            node_list.append(node)

        return node_list
