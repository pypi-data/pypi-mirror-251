from src.hostfm import HostFile
from src.hostfm.type import HostEntry
from ipaddress import IPv4Address


def test_read_host():
    host = HostFile()
    assert type(host.entries) is list
    for item in host.entries:
        assert type(item.ip) is IPv4Address
        assert type(item.host) is str
        assert type(item.aliases) is list

