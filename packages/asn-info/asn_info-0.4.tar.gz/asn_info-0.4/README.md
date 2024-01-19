# ASN Info
A python library providing information about ASNs (AS Name, Country and MANRS membership)

This library downloads the Autonomous System list and information from RIPE NCC and provides its contents as objects.

There are three data points:

- Autonomous System Name: *get_as_name()*
- Autonomous System Country: *get_as_country()*
- Wether an ASN is a MANRS Participant: *is_manrs_participant()*

MANRS Data is not loaded by default, since it requires an API key.  In case you want to load it, you will have to prepare a .env file containing a line like this:

```shell
MANRS_API_KEY=ad83444d-4c68-4727-9ff6-ce2df6649c05
```

You can obtain an API key [here](https://www.manrs.org/resources/api/)

Example use:

```python
import asn_info

asn_data = asn_info.Asns()

h = asn_data.load_asn_data(add_manrs_data=True)

print(asn_data.get_as_name(58280))
print(asn_data.get_as_country(58280))
print(asn_data.is_manrs_participant(58280))

```

Result:

```shell
STUCCHIMAX-AS Massimiliano Andrea Stucchi
CH
False
```

You can also filter the ASNs per country, as follows:

```python
switzerland = asn_data.asns_per_country("CH")

for asn in switzerland:
    print("{} has {}".format(asn, switzerland[asn]))
```

Output:

```
...
58280 has {'country': 'CH', 'as_name': 'STUCCHIMAX-AS Massimiliano Andrea Stucchi'}
...
```

