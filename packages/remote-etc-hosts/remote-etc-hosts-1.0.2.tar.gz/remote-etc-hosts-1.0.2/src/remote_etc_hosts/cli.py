import json
import os
import typing as t

import fire

from remote_etc_hosts.api import RemoteHosts


class RemoteHostsCli:
    """parse and operate /etc/hosts in remote host."""

    def __init__(self, ip: str, password: t.Optional[str] = None, username: t.Optional[str] = None) -> None:

        # get username and password from env
        os_user = os.getenv("REMOTE_HOST_SSH_USER")
        os_password = os.getenv("REMOTE_HOST_SSH_PASSWORD")

        # 2 of 1
        assert password or os_password, \
            'You need to provide the password either as a parameter or as an environment \
                variable REMOTE_HOST_SSH_PASSWORD'
        assert username or os_user, \
            'You need to provide the username either as a parameter or as an environment variable REMOTE_HOST_SSH_USER'

        self.ip = ip
        self.username = username if username else os_user
        self.password = password if password else os_password

        self.__remote_hosts_ins = RemoteHosts(ip=self.ip, username=self.username, password=self.password)

    @staticmethod
    def __print_ip_domains(data: dict):
        # can not serialize set by default, so convert value to list
        print(json.dumps({key: list(value) for key, value in data.items()}, indent=4))

    def ip_domains(self):
        """Get the mapping relationship from IP to domains."""
        data = self.__remote_hosts_ins.ip_domains
        self.__print_ip_domains(data)

    def domain_ip(self):
        """Get the mapping relationship from DOMAIN to ip."""
        print(json.dumps(self.__remote_hosts_ins.domain_ip, indent=4))

    def query_domains_by_ip(self, q_ip: str):
        """query domains by ip you offer"""
        print(json.dumps(list(self.__remote_hosts_ins.query_domains_by_ip(q_ip)), indent=4))

    def query_ip_by_domain(self, q_domain: str):
        """query ip by domain you offer"""
        print(self.__remote_hosts_ins.query_ip_by_domain(q_domain))

    def add_item(self, n_ip: str, n_domains: t.Union[set, list]):
        """add new item to /etc/hosts"""
        data = self.__remote_hosts_ins.add_item(n_ip, n_domains)
        self.__print_ip_domains(data)

    def delete_item_by_ip(self, d_ip: str):
        """delete item from /etc/hosts by ip"""
        data = self.__remote_hosts_ins.delete_item_by_ip(d_ip)
        self.__print_ip_domains(data)

    def delete_item_by_domain(self, d_domain: str):
        """delete item from /etc/hosts by domain"""
        data = self.__remote_hosts_ins.delete_item_by_domain(d_domain)
        self.__print_ip_domains(data)


def main():
    fire.Fire(RemoteHostsCli)


if __name__ == "__main__":
    main()
