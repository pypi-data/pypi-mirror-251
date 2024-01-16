class EmptyHosts(Exception):
    def __str__(self) -> str:
        return "non content found in `/etc/hosts`"


class ItemNotFound(Exception):
    def __init__(self, ip):
        self.ip = ip

    def __str__(self) -> str:
        return f"item {self.ip} not found in /etc/hosts"
