# wedos-wapi-client

Wrapper around [WEDOS WAPI](https://kb.wedos.com/kategorie/wapi-api-interface/)

(Note: WAPI must be enabled for your account and your IP must be authorized to access it.)

Example usage for DNS:

```python
from wedos_wapi_client import WapiClient

old_ip = "1.2.3.4"
new_ip = "10.20.30.40"

wapi = WapiClient(user="your-email@domain.tld", password="secret-password")

for domain in wapi.domains_list().data["domain"].values():
    for row in wapi.dns_rows_list(domain["name"]).data["row"]:
        if row["rdtype"] == "A" and row["rdata"] == old_ip:
            wapi.dns_row_update(domain=domain["name"], row_id=row["ID"], rdata=new_ip)
    wapi.dns_domain_commit(name=domain["name"])
```
