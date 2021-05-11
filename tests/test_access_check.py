
# Fudge the python path
import sys
import os
from typing import Any, Dict
from collections import defaultdict

import pandas as pd
import pytest
import re


PACKAGE_PARENT = '../../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# end fudge python path

from plugins.batfish.includes.access_check import AccessCheck


# INPUTS

# IP's
src_ip = "10.1.255.100"
destination_ip = "10.3.255.100"

# Services
#applications =["dns"]
applications =["icmp"]
#applications = ["https"]

# Nodes to query
nodes = "spoke1"
node_list = ["spoke1", "spoke2"]

class AcceptResult(object):

    def __init__(self, 

            query_node=None, 
            flow_result=None,
            flow_details=None,
            trace_tree_list=None,
            ingress_egress=None,
            ingress_interface=None,
            egress_interface=None,
            ingress_vrf=None,
            ingress_node=None,
            source_address=None,
            destination_address=None,
            service=None,
            ip_protocol=None,
            permit_rule=None,
            rule_id=None,
            result_data=None


            ) -> None:
        pass
        
        self.query_node = query_node
        self.flow_result = flow_result
        self.flow_details = flow_details
        self.trace_tree_list = trace_tree_list
        self.ingress_egress = ingress_egress
        self.ingress_interface = ingress_interface
        self.egress_interface = egress_interface
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

    def __init__(self, 

            query_node=None, 
            denied=None,

            ) -> None:
        pass
        
        self.query_node = query_node  
        self.denied = True


@pytest.mark.batfish
def main():

    ac = AccessCheck()

    
    results = ac.check(src_ip=src_ip, destination_ip=destination_ip, applications=applications, nodes=nodes, snapshot_folder="/shared/data/storage/firewall-configs/snapshot")
    
    all_results = []

    

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)

    #show_all(results)
    #show_permitted(results)
    #show_denied(results)
    #show_permitted_all(all_results)

    result_dict = _build_results_dict(ac)

    # build new access_result object
    access_results = _build_access_result(result_dict)
    print(access_results)



def show_all(results):
    # print all results
    for v in results.values:
        for enum, e in enumerate(v):
            if enum == 0:
                print(f"Node Queried is: {e}")
            if enum == 1:
                print(f"From zone/iface to zone/iface: {e}")
            if enum == 2:
                print(f"Flow details: {e}")
            if enum == 3:
                print(f"Flow result : *** {e} ***")
            if enum == 4:
                pass
            if enum == 5:
                print(f"TraceTreeList: {e}")

            

def show_permitted(results):

    # print only if accepted/permitted
    for v in results.values:
        if re.search("permit", v[3], re.IGNORECASE):
            if len(v[5]) > 0:
                for item in v[5]:
                    for item_child in item.children:
                        for c in item_child.children:
                            if re.search('permitted', c.traceElement.fragments[0].text, re.IGNORECASE):
                                for enum, e in enumerate(v):
                                    if enum == 3:
                                        print("========================")
                                        print(f"Flow result : *** {e} ***")
                                        continue
                                    if enum == 0:
                                        print(f"Node Queried is: {e}")
                                    if enum == 1:
                                        print(f"From zone/iface to zone/iface: {e}")
                                    if enum == 2:
                                        print(f"Flow details: {e}")
                                    if enum == 4:
                                        pass
                                    if enum == 5:
                                        print(f"TraceTreeList: {e}")
                                        print("========================")


def show_permitted_all(all_results):

    hits: int = 0
    # print only if accepted/permitted
    for result in all_results:
        for v in result.values:
            if re.search("permit", v[3], re.IGNORECASE):
                if len(v[5]) > 0:
                    for item in v[5]:
                        for item_child in item.children:
                            for c in item_child.children:
                                if re.search('permitted', c.traceElement.fragments[0].text, re.IGNORECASE):
                                    hits +=1
                                    for enum, e in enumerate(v):
                                        if enum == 3:
                                            print("========================")
                                            print(f"Flow result : *** {e} ***")
                                            continue
                                        if enum == 0:
                                            print(f"Node Queried is: {e}")
                                        if enum == 1:
                                            print(f"From zone/iface to zone/iface: {e}")
                                        if enum == 2:
                                            print(f"Flow details: {e}")
                                        if enum == 4:
                                            pass
                                        if enum == 5:
                                            print(f"TraceTreeList: {e}")
                                            print("========================")
    if hits == 0:
        print(f"DENIED ON HOST: ")



def show_denied(results):

    # print only if accepted/permitted
    for v in results.values:
        if "DENY" in v[3]:
            for enum, e in enumerate(v):
                if enum == 3:
                    print(f"Flow result : *** {e} ***")
                    continue
                if enum == 0:
                    print(f"Node Queried is: {e}")
                if enum == 1:
                    print(f"From zone/iface to zone/iface: {e}")
                if enum == 2:
                    print(f"Flow details: {e}")
                if enum == 4:
                    pass
                if enum == 5:
                    print(f"TraceTreeList: {e}")

def _build_results_dict(ac) -> Dict[str, Any]:

    results_dict = defaultdict(list)

    for node in node_list:
        result = ac.check(src_ip=src_ip, destination_ip=destination_ip, applications=applications, nodes=node, snapshot_folder="/shared/data/storage/firewall-configs/snapshot")
        results_dict[node].append(result)

    return results_dict

def _build_access_result(results_dict) -> AcceptResult:

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
                                    if re.search('permitted', c.traceElement.fragments[0].text, re.IGNORECASE):
                                        for enum, e in enumerate(v):
                                            if enum == 3:
                                                print("========================")
                                                print(f"Flow result : *** {e} ***")
                                                access_result.flow_result = e
                                                continue
                                            if enum == 0:
                                                print(f"Node Queried is: {e}")
                                            
                                            if enum == 1:
                                                print(f"From zone/iface to zone/iface: {e}")
                                                access_result.ingress_egress = e
                                            if enum == 2:
                                                print(f"Flow details: {e}")
                                                access_result.flow_details = e
                                                # other details
                                                access_result.destination_address = access_result.flow_details.dstIp
                                                access_result.source_address = access_result.flow_details.srcIp
                                                access_result.service = access_result.flow_details.ipProtocol
                                                access_result.ingress_node = access_result.flow_details.ingressNode
                                                access_result.ingress_vrf = access_result.ingress_vrf
                                            if enum == 4:
                                                pass
                                            if enum == 5:
                                                print(f"TraceTreeList: {e}")
                                                print("========================")
                                                access_result.trace_tree_list = e
                                                # get policy permit details / rule details
                                                access_result.permit_rule = access_result.trace_tree_list[0].traceElement.fragments[1].text
                                                access_result.rule_id = access_result.trace_tree_list[0].traceElement.fragments[2].text

                                            
                    
                    if access_result.flow_result == "PERMIT":
                        access_results.append(access_result)


                else:
                    # todo - generate a DENY entry
                    
                    denied_result = DeniedResult()

                    denied_result.denied == True
                    denied_result.query_node = node

                    denied_results.append(denied_result)
                

    merged_results = [*access_results, *denied_results]

    
                    



    return merged_results








if __name__ == "__main__":
    main()