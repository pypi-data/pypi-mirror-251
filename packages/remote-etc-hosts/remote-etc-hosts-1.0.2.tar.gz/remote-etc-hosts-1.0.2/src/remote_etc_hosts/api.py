import typing as t
from collections import defaultdict

import paramiko
from paramiko import SSHClient

from remote_etc_hosts.exceptions import ItemNotFound
from remote_etc_hosts.utils import parse_hosts


class RemoteHosts:
    def __init__(self, ip: str, username: str, password: str) -> None:
        self.ip = ip
        self.username = username
        self.password = password
        # one ip have multi domains
        self._ip_domains = defaultdict(lambda: set())
        # one domain have one ip
        self._domain_ip = defaultdict(lambda: "")
        self._ssh_client = None
        self._raw_hosts = ""
        self._fresh = False

    @property
    def ip_domains(self) -> dict:
        """
        return eg:
        {
            "10.1.1.1": {"dnsA", "dnsB"},
            "10.1.1.2": {"dnsC", "dnsD"},
        }
        """
        if not self._ip_domains:
            self._parse_hosts()
        return self._ip_domains

    @property
    def domain_ip(self) -> dict:
        """
        return eg:
        {
            "dnsA": "10.1.1.1",
            "dnsB": "10.1.1.1",
            "dnsC": "10.1.1.2",
            "dnsD": "10.1.1.2"
        }
        """
        if not self._domain_ip:
            self._parse_hosts()
        return self._domain_ip

    def query_domains_by_ip(self, ip: str) -> t.Optional[set]:
        """
        return eg:
        {"dnsA", "dnsB"} or None
        """
        return self.ip_domains.get(ip)

    def query_ip_by_domain(self, domain) -> t.Optional[str]:
        """
        return eg:
        "10.1.1.1" or None
        """
        return self.domain_ip.get(domain)

    def add_item(self, ip, domains: t.Union[list, set]) -> dict:
        # add data in self.ip_domains
        self.ip_domains[ip] |= set(domains)

        # add data in self.domain_ip
        for d in domains:
            self.domain_ip[d] = ip

        self._write_to_hosts()
        return self.ip_domains

    def delete_item_by_ip(self, ip: str) -> dict:
        if ip not in self.ip_domains.keys():
            raise ItemNotFound(ip)

        domains = self.ip_domains[ip]
        # delete data in self.ip_domains
        del self.ip_domains[ip]

        # delete data in self.domain_ip
        for d in domains:
            del self.domain_ip[d]

        self._write_to_hosts()
        return self.ip_domains

    def delete_item_by_domain(self, domain: str) -> dict:
        if domain not in self.domain_ip.keys():
            raise ItemNotFound(domain)

        ip = self.domain_ip[domain]
        # delete data in self.domain_ip
        del self.domain_ip[domain]

        # delete data in self.ip_domains
        origin_domains = self.ip_domains[ip]
        filterd_domains = set(filter(lambda x: x != domain, origin_domains))
        # domain is empty, delte ip item
        if not filterd_domains:
            del self.ip_domains[ip]
        else:
            self.ip_domains[ip] = filterd_domains

        self._write_to_hosts()
        return self.ip_domains

    @property
    def ssh_client(self) -> SSHClient:
        if self._ssh_client is None:
            ssh_client = paramiko.SSHClient()
            ssh_client.load_system_host_keys()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(
                hostname=self.ip,
                username=self.username,
                password=self.password,
                timeout=10,
                banner_timeout=30,
            )
            self._ssh_client = ssh_client
        return self._ssh_client

    @property
    def raw_hosts(self) -> str:
        if not self._raw_hosts or self._fresh is True:
            _, out, _ = self.ssh_client.exec_command("cat /etc/hosts | grep -v ^# | grep -v ^$")
            raw_hosts = out.read().decode("utf-8")
            self._raw_hosts = raw_hosts
            self._fresh = False
        return self._raw_hosts

    def _parse_hosts(self):
        hosts_info = parse_hosts(self.raw_hosts)
        for ip, domain in hosts_info:
            # fill in ip_domains
            self._ip_domains[ip] |= set(domain)
            for d in domain:
                # fill in domain_ip
                self._domain_ip[d] = ip

    def _write_to_hosts(self):
        etc_hosts = ""
        for key, value in self.ip_domains.items():
            etc_hosts += f"{key} {' '.join(list(value))}\n"
        self.ssh_client.exec_command(f"echo '{etc_hosts}' > /etc/hosts")
        self._fresh = True

    def __str__(self) -> str:
        return self.raw_hosts

    def __repr__(self) -> str:
        return str(self)
