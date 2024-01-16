import re
from typing import List

from remote_etc_hosts.exceptions import EmptyHosts


def parse_hosts(raw_hosts: str) -> List[tuple]:
    data = raw_hosts.strip()
    if not data:
        raise EmptyHosts()
    data = data.split("\n")
    results = []
    for line in data:
        single_data = re.split(r"\s+", line.strip())
        if single_data:
            ip, domains = single_data[0], single_data[1:]
            results.append((ip, domains))
    return results
