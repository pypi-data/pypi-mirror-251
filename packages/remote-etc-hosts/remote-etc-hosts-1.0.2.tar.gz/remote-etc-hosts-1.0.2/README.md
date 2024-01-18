# remote-hosts

This is a simple tool for parsing `/etc/hosts` file in remote hosts.
Sure, It's very very simple but useful for someone need it. I just want to learn something from this wheel, :)

You can do these things if you install it.

## API

1. get total view of /etc/hosts

```python
from remote_hosts import RemoteHosts
ins = RemoteHosts(ip="192.168.101.1", username="root", password="xxx")
print(dict(ins.ip_domains))
print(dict(ins.domain_ip))
```

2. query domain by ip

```python
print(ins.query_domains_by_ip("192.168.101.2"))
```

3. query ip by domain

```python
print(ins.query_ip_by_domain("domainA"))
```

4. add a new item to `/etc/hosts`

```python
ins.add_item("192.168.10.1", ["dnsA", "dnsB"])
print(dict(ins.domain_ip))
print(dict(ins.ip_domains))
```

5. del item by ip

```python
ins.delte_item_by_ip("192.168.10.1")
print(dict(ins.domain_ip))
print(dict(ins.ip_domains))
```

6. del item by domain

```python
ins.delete_item_by_domain("dnsB")
print(dict(ins.domain_ip))
print(dict(ins.ip_domains))
```

## CLIs

we also offer you some CLIs as same as api mentioned above:

Note: You can ignore the `--password` and `--username` parameter by setting the environment parameter: REMOTE_HOST_SSH_USER and REMOTE_HOST_SSH_PASSWORD

1. get total view of /etc/hosts

```bash
remote_etc_hosts --ip 192.168.0.1 --password xxx --username root ip_domains
remote_etc_hosts --ip 192.168.0.1 --password xxx --username root domain_ip
```

2. query domain by ip

```bash
remote_etc_hosts --ip 192.168.0.1 --password xxx --username root query_domain_by_ip 127.0.0.1
```

3. query ip by domain

```bash
remote_etc_hosts --ip 192.168.0.1 --password xxx --username root query_ip_by_domain dnsA
```

4. add a new item to `/etc/hosts`

```bash
remote_etc_hosts --ip 192.168.0.1 --password xxx --username root add_item 192.168.0.2 '[dnsA, dnsB]'
```

5. del item by ip

```bash
remote_etc_hosts --ip 192.168.0.1 --password xxx --username root delete_item_by_ip 192.168.0.2
```

6. del item by domain

```bash
remote_etc_hosts --ip 192.168.0.1 --password xxx --username root delete_item_by_domain dnsA
```

# install

note: python3.10 or above is needed!

```bash
pip install remote-etc-hosts
```
