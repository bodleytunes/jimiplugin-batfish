from logging import exception
from typing import Optional, List, Tuple, DefaultDict, Any
import re
from collections import defaultdict

import pandas as pd

from pybatfish.exception import BatfishException

from plugins.batfish.includes.batfish import Batfish
from plugins.batfish.includes.result_models.access import AcceptResult, DeniedResult
from plugins.batfish.includes.bat_helpers import BatHelpers
from plugins.batfish.includes.data.builder import AccessDataBuilder


class AccessCheck(Batfish):
    def __init__(
        self,
        batfish_server: Optional[str] = None,
        host: Optional[str] = None,
        src_ip: Optional[str] = None,
        dst_ip: Optional[str] = None,
        applications: Optional[list] = None,
        dst_ports: Optional[str] = None,
        ip_protocols: List[Any] = None,
        nodes: Optional[str] = None,
        snapshot_folder: Optional[str] = None,
        b_fish=None,
    ):

        self.batfish_server = batfish_server
        self.host = host
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.applications = applications
        self.dst_ports = dst_ports
        self.ip_protocols = ip_protocols
        self.snapshot_folder = snapshot_folder
        # self.nodes = "hub2"

        # Instance of a batfish object
        self.b_fish = b_fish

        pass

    def get_results(
        self,
        src_ip: Optional[str] = None,
        dst_ip: Optional[str] = None,
        applications: Optional[list] = None,
        dst_ports: Optional[str] = None,
        ip_protocols: List[Any] = None,
        nodes: Optional[list] = None,
    ) -> Tuple[List[dict], List[dict]]:
        """Get Batfish Results

        Args:
            src_ip (string, optional): source ip. Defaults to None.
            dst_ip (string, optional): destination ip. Defaults to None.
            applications (list, optional): list of applications. Defaults to None.
            dst_ports (str, optional): list of destination ports. Defaults to None.
            ip_protocols (list, optional): list of protocols. Defaults to None.
            nodes (list, optional): list of nodes(network devices/firewalls etc)to query. Defaults to None.

        Returns:
            Tuple[List[dict], List[dict]]: 2 variables, each a list of dictionaries for permitted and denied results
        """

        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.applications = applications
        self.dst_ports = dst_ports
        self.ip_protocols = ip_protocols
        self.nodes = nodes

        # make pre-check and validation on input data
        self._pre_flight_checks()

        # create empty list for returned results (Accept and Deny results)
        self.results_dict = defaultdict(list)

        # Loop through all passed in nodes(Network devices/Firewalls)
        for node in self.nodes:

            # Run access checker function to make the batfish query on a per node basis and return a result for each of them
            self._query(node)

            # Append each nodes query result to the list
            # results_dict[node].append(result)

        # process results (walk dataframe) and return dictionary type data suitable for merging with eventData
        (
            deny_results,
            accept_results,
        ) = self._build_results(self.results_dict)

        # return both deny and results variables to "action"
        return deny_results, accept_results

    def _pre_flight_checks(self):

        # validate IP's
        if self.src_ip:
            self.src_ip = BatHelpers.check_valid_ip(self.src_ip)
        if self.dst_ip:
            self.dst_ip = BatHelpers.check_valid_ip(self.dst_ip)
        # validate ports
        # validate protocols
        # validate apps

        # sanity check source and destination exist
        if not self.src_ip and not self.dst_ip:
            raise exception("Need to have at least a source or dest IP")
        # empty source/dest changed to 0.0.0.0/0
        if not self.src_ip:
            self.src_ip = "0.0.0.0/0"
        if not self.dst_ip:
            self.dst_ip = "0.0.0.0/0"

    def _query(self, nodes: Optional[list] = None) -> pd.DataFrame:
        """Do Batfish Query

        Args:
            nodes (list, optional): list of nodes to query. Defaults to None.

        Raises:
            BatfishException: batfish exception

        Returns:
            pd.DataFrame: returns nested structured data frame
        """
        if len(self.applications) > 0:

            # flow is a headerConstraint object which was built from passing in args relating to the source/dst ip/proto (5 tuple etc)
            flow = self.b_fish.hc(
                srcIps=self.src_ip, dstIps=self.dst_ip, applications=self.applications
            )
        elif len(self.dst_ports) > 0 and len(self.ip_protocols) > 0:
            # send dst_ports to splitter helper
            self.dst_ports_list = BatHelpers._split_ports(self.dst_ports)
            # there are more than one port returned in the list then loop through ports and make a query on each one
            if len(self.dst_ports_list) > 1:
                print("multiple ports")
                for port in self.dst_ports_list:
                    flow = self.b_fish.hc(
                        srcIps=self.src_ip,
                        dstIps=self.dst_ip,
                        dstPorts=port,
                        ipProtocols=BatHelpers.make_upper(self.ip_protocols),
                    )
                    self._make_query(flow, nodes)

            flow = self.b_fish.hc(
                srcIps=self.src_ip,
                dstIps=self.dst_ip,
                dstPorts=self.dst_ports,
                ipProtocols=BatHelpers.make_upper(self.ip_protocols),
            )
            self._make_query(flow, nodes)
        elif len(self.dst_ports) > 0:
            flow = self.b_fish.hc(
                srcIps=self.src_ip,
                dstIps=self.dst_ip,
                dstPorts=self.dst_ports,
            )
            self._make_query(flow, nodes)

        elif len(self.ip_protocols) > 0:
            flow = self.b_fish.hc(
                srcIps=self.src_ip,
                dstIps=self.dst_ip,
                ipProtocols=self.ip_protocols,
            )
            self._make_query(flow, nodes)

    def _make_query(self, flow, nodes):
        """
        make query
        """
        # nodes is actually a single node here, not sure why batfish have named it "nodes"?
        # flow is a headerConstraint object which was built from passing in args relating to the source/dst ip/proto (5 tuple etc)
        try:
            query = self.b_fish.bfq.testFilters(headers=flow, nodes=nodes)
            result = query.answer().frame()
            # Append each nodes query result to the results_dict list
            self.results_dict[nodes].append(result)

        except BatfishException as e:
            print(e)
            raise BatfishException(f"Batfish Query failure :  {e}")

    def _build_results(
        self, results_dict: DefaultDict[str, List[Any]]
    ) -> Tuple[List[dict], List[dict]]:
        """Build event data results

        Args:
            results_dict (List[pd.DataFrame]): Pass in list of dataframes (one per node)

        Returns:
            Tuple[List[dict], List[dict]]: 2 Lists of dicts for denied results and accept results
        """
        data_builder = AccessDataBuilder()
        data_builder.build_data(results_dict)
        return data_builder.deny_results, data_builder.accept_results
