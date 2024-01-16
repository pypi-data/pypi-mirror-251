import os

try:
    from utils import parse_host_entry
    from type import HostEntry
except ImportError:  # for pytest
    from hostfm.utils import parse_host_entry
    from hostfm.type import HostEntry


class HostFile:
    def __init__(self, path: str = None) -> None:
        self.entries: list[HostEntry] = []
        self.read(path=path)
        
    def read(self, path: str = None):
        HOST_FILE_PATH = path or os.path.join(os.environ.get("SYSTEMROOT"), "System32", "drivers", "etc", "hosts")
        if not os.path.exists(HOST_FILE_PATH):
            raise FileNotFoundError(f"Host file not found: {HOST_FILE_PATH}")
        self.entries = []
        with open(HOST_FILE_PATH) as hosts:
            for i, line in enumerate(hosts.readlines()):
                if not line.startswith("#"):
                    host = parse_host_entry(line, line_no=i)
                    if host:
                        self.entries.append(host)


    