'''
# CDKTF prebuilt bindings for hashicorp/opc provider version 1.4.1

HashiCorp made the decision to stop publishing new versions of prebuilt [Terraform opc provider](https://registry.terraform.io/providers/hashicorp/opc/1.4.1) bindings for [CDK for Terraform](https://cdk.tf) on January 16, 2024. As such, this repository has been archived and is no longer supported in any way by HashiCorp. Previously-published versions of this prebuilt provider will still continue to be available on their respective package managers (e.g. npm, PyPi, Maven, NuGet), but these will not be compatible with new releases of `cdktf` past `0.20.0` and are no longer eligible for commercial support.

As a reminder, you can continue to use the `hashicorp/opc` provider in your CDK for Terraform (CDKTF) projects, even with newer versions of CDKTF, but you will need to generate the bindings locally. The easiest way to do so is to use the [`provider add` command](https://developer.hashicorp.com/terraform/cdktf/cli-reference/commands#provider-add), optionally with the `--force-local` flag enabled:

`cdktf provider add hashicorp/opc --force-local`

For more information and additional examples, check out our documentation on [generating provider bindings manually](https://cdk.tf/imports).

## Deprecated Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-opc](https://www.npmjs.com/package/@cdktf/provider-opc).

`npm install @cdktf/provider-opc`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-opc](https://pypi.org/project/cdktf-cdktf-provider-opc).

`pipenv install cdktf-cdktf-provider-opc`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Opc](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Opc).

`dotnet add package HashiCorp.Cdktf.Providers.Opc`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-opc](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-opc).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-opc</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-opc-go`](https://github.com/cdktf/cdktf-provider-opc-go) package.

`go get github.com/cdktf/cdktf-provider-opc-go/opc`

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-opc).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

__all__ = [
    "compute_acl",
    "compute_image_list",
    "compute_image_list_entry",
    "compute_instance",
    "compute_ip_address_association",
    "compute_ip_address_prefix_set",
    "compute_ip_address_reservation",
    "compute_ip_association",
    "compute_ip_network",
    "compute_ip_network_exchange",
    "compute_ip_reservation",
    "compute_machine_image",
    "compute_orchestrated_instance",
    "compute_route",
    "compute_sec_rule",
    "compute_security_application",
    "compute_security_association",
    "compute_security_ip_list",
    "compute_security_list",
    "compute_security_protocol",
    "compute_security_rule",
    "compute_snapshot",
    "compute_ssh_key",
    "compute_storage_attachment",
    "compute_storage_volume",
    "compute_storage_volume_snapshot",
    "compute_vnic_set",
    "compute_vpn_endpoint_v2",
    "data_opc_compute_image_list_entry",
    "data_opc_compute_ip_address_reservation",
    "data_opc_compute_ip_reservation",
    "data_opc_compute_machine_image",
    "data_opc_compute_network_interface",
    "data_opc_compute_ssh_key",
    "data_opc_compute_storage_volume_snapshot",
    "data_opc_compute_vnic",
    "lbaas_certificate",
    "lbaas_listener",
    "lbaas_load_balancer",
    "lbaas_policy",
    "lbaas_server_pool",
    "provider",
    "storage_container",
    "storage_object",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import compute_acl
from . import compute_image_list
from . import compute_image_list_entry
from . import compute_instance
from . import compute_ip_address_association
from . import compute_ip_address_prefix_set
from . import compute_ip_address_reservation
from . import compute_ip_association
from . import compute_ip_network
from . import compute_ip_network_exchange
from . import compute_ip_reservation
from . import compute_machine_image
from . import compute_orchestrated_instance
from . import compute_route
from . import compute_sec_rule
from . import compute_security_application
from . import compute_security_association
from . import compute_security_ip_list
from . import compute_security_list
from . import compute_security_protocol
from . import compute_security_rule
from . import compute_snapshot
from . import compute_ssh_key
from . import compute_storage_attachment
from . import compute_storage_volume
from . import compute_storage_volume_snapshot
from . import compute_vnic_set
from . import compute_vpn_endpoint_v2
from . import data_opc_compute_image_list_entry
from . import data_opc_compute_ip_address_reservation
from . import data_opc_compute_ip_reservation
from . import data_opc_compute_machine_image
from . import data_opc_compute_network_interface
from . import data_opc_compute_ssh_key
from . import data_opc_compute_storage_volume_snapshot
from . import data_opc_compute_vnic
from . import lbaas_certificate
from . import lbaas_listener
from . import lbaas_load_balancer
from . import lbaas_policy
from . import lbaas_server_pool
from . import provider
from . import storage_container
from . import storage_object
