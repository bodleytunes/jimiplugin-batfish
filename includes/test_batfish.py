from batfish import batfish

SRC_IP = "10.1.255.100"
# DST_IP = "10.3.255.100"
DST_IP = "8.8.8.8"
DST_PORT = "53"
APPLICATIONS = ["dns", "ssh"]
IP_PROTOCOLS = ["tcp", "udp"]

b = batfish(
    src_ip=SRC_IP,
    dst_ip=DST_IP,
    dst_port=DST_PORT,
    device_type=None,
    BATFISH_NETWORK=None,
    BATFISH_SERVER=None,
)
b.get_configs()
answers = b.get_data()


def test_print_results(answers):
    traceroutes = answers
    # traces = traceroutes.Traces.iloc
    for t in traceroutes:
        print("================================================================")
        # Destination Network
        # Source device
        # print(f"Traffic sourced from:  {t.Traces.iloc[0].hops[0].node}")
        print(f"Traffic sourced from:  {t.Traces.values[0][0].hops[0].node}")
        print("---------------------------------------------------------------")
        print(f"Traffic Destination: {b.dst_ip}")
        print("---------------------------------------------------------------")
        # Egress interface
        # print(
        #    f"Next-hop (Egress) interface: {t.Traces.iloc[0].hops[0].steps[3].detail}"
        # )
        # print(
        #    f"Next-hop (Egress) interface: {t.Traces.values[0][0].hops[0].steps[3].detail}"
        # )
        # Loop through egress ifaces
        for hop in t.Traces.values[0]:
            print(f"Next-hop (Egress) interface: {hop.hops[0].steps[3].detail}")
        # Next-hop interface
        # print(
        #    f"Next-hop IP:  {t.Traces.iloc[0].hops[0].steps[1].detail.routes[0]['nextHopIp']}"
        # )
        # Print ECMP next-hop #1
        # print(
        #    f"Next-hop IP:  {t.Traces.values[0][0].hops[0].steps[1].detail.routes[0]['nextHopIp']}"
        # )
        ## Print ECMP next-hop #2
        # print(
        #    f"Next-hop IP:  {t.Traces.values[0][1].hops[0].steps[1].detail.routes[0]['nextHopIp']}"
        # )
        # Loop through ECMP hops
        for hop in t.Traces.values[0]:
            print(f"Next-hop IP:  {hop.hops[0].steps[1].detail.routes[0]['nextHopIp']}")
        # Next-hop protocol
        # print(
        #    f"Protocol/route type: {t.Traces.values[0][0].hops[0].steps[1].detail.routes[0]['protocol']}"
        # )
        # Loop through protocols
        for hop in t.Traces.values[0]:
            print(
                f"Protocol/route type: {hop.hops[0].steps[1].detail.routes[0]['protocol']}"
            )
        print("================================================================")
        # Is Permitted


test_print_results(answers)