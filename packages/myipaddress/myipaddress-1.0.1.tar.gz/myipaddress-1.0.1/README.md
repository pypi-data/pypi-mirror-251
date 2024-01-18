# myIPaddress 🌎

### Module Overview:

This module provides functionality to fetch IP information, including public and private IP addresses, location details, open ports, and more.

## How to Use:

- `myIPaddress.{function_name}()`

### Public IP:

- **`.info`** - Returns all public information in JSON format.

- **`.public_ip()`** - Returns the public IP address.

- **`.public_hostname()`** - Returns the public hostname.

- **`.public_city()`** - Returns the public city.

- **`.public_region()`** - Returns the public region.

- **`.public_country()`** - Returns the public country.

- **`.public_loc()`** - Returns the public location.

- **`.public_organization()`** - Returns the public organization.

- **`.public_postal()`** - Returns the public postal code.

- **`.public_fulladdress()`** - Returns a formatted string of public city, region, country, and postal code.

- **`.public_timezone()`** - Returns the public timezone.

 ### Private IP:

- **`.private_ip()`** - Returns the private IP address.

 ### Other Networking Information:

- **`.open_ports()`** - Returns a list of open ports on the local machine.

- **`.ip_probe(ip_address, indent=False)`** - Retrieves IP information for a specified IP address using the "https://ipinfo.io/{ip_address}/json" API.

### Example Usage:

Example:

```python
import myIPaddress as myip

ip_info = myip.public_ip()
print(f"Public IP Address: {ip_info}")
```

Output:

```python
Public IP Address: 8.8.8.8
