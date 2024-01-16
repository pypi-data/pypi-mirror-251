import ipaddress
import re

try:
    from type import HostEntry
    from errors import InvalidHostEntry, InvalidIPAdrees, InvalidDomain
except ImportError:  # for pytest
    from hostfm.type import HostEntry
    from hostfm.errors import InvalidHostEntry, InvalidIPAdrees, InvalidDomain
    


def _is_valid_ip(ip: str):
    try:
        # check for valid ip address
        return ipaddress.ip_address(ip)
    except ValueError as e:
        raise InvalidIPAdrees(*e.args) from None


def _is_valid_host(host: str):
    # TODO: Implement host validation
    return host


def parse_host_entry(host: str, **kwargs) -> HostEntry:
    if not host.strip():
        return # return if host is blank line
    
    PATTERN = r"(?P<ip>[\d.]+)([\s]+)(?P<dn>[\S]+)([\s]*)(?P<aliases>.*)"
    
    host_parts = re.match(PATTERN, host.strip())
    if not host_parts:
        raise InvalidHostEntry(f"`{host}`")
    host_parts = host_parts.groupdict()
    ip = _is_valid_ip(host_parts['ip'])
    dn = _is_valid_host(host_parts['dn'])
    aliases = [_is_valid_host(a) for a in host_parts['aliases'].split()]

    entry = HostEntry(ip, dn, aliases, **kwargs)

    return entry



if __name__ == "__main__":
    print(parse_host_entry("         \n"))
    parse_host_entry("192.168.1.1    example.com    alias1 alias2")
    parse_host_entry("192.168.1.1    example#com")
    parse_host_entry("192.168.1.1 d")
    parse_host_entry("192.168.1.111 sdf")

    