from typing import Any, List
import ipaddress


class BatHelpers:
    """Helper Class for Batfish Queries"""

    @staticmethod
    def check_valid_ip(arg: Any) -> Any:
        try:
            arg = format(ipaddress.IPv4Address(arg))
        except (ValueError, TypeError) as e:
            raise ValueError(f"invalid IP: {e}")

        return arg

    @staticmethod
    def filter_text(arg: List[Any]) -> List[Any]:
        if arg:

            def converter(i):
                return i or None

            result = [converter(i) for i in arg]
            return result
        return arg

    @staticmethod
    def make_upper(arg: List[Any]) -> List[Any]:
        if arg:
            result = [x.upper() for x in arg]
            return result
        return arg
