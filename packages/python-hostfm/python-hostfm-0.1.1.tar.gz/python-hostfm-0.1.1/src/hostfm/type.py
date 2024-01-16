

class HostEntry:
    def __init__(self, ip: str = None, host: str = None, aliases: list[str]=None, **kwargs) -> None:
        self.ip = ip
        self.host = host
        self.aliases = aliases

        for k, v in kwargs.items():
            self.__dict__[f"_{k}"] = v
    
    # Todo: Add modify, remove methods
    

    def __repr__(self) -> str:
        return f"{self.ip} - {self.host} - {self.aliases}"
