# pyzabbix

Python client for using Zabbix API

## Example

```python
import pyzabbix

zapi = ZabbixAPI('http://localhost')

user = 'xxx'
password = 'yyy'
zapi.login(user=user, passowrd=password)

host = zapi.host.get()
```
