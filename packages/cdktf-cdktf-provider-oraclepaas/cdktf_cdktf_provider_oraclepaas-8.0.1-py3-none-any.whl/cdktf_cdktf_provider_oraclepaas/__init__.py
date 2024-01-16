'''
# CDKTF prebuilt bindings for hashicorp/oraclepaas provider version 1.5.3

HashiCorp made the decision to stop publishing new versions of prebuilt [Terraform oraclepaas provider](https://registry.terraform.io/providers/hashicorp/oraclepaas/1.5.3) bindings for [CDK for Terraform](https://cdk.tf) on January 15, 2024. As such, this repository has been archived and is no longer supported in any way by HashiCorp. Previously-published versions of this prebuilt provider will still continue to be available on their respective package managers (e.g. npm, PyPi, Maven, NuGet), but these will not be compatible with new releases of `cdktf` past `0.20.0` and are no longer eligible for commercial support.

As a reminder, you can continue to use the `hashicorp/oraclepaas` provider in your CDK for Terraform (CDKTF) projects, even with newer versions of CDKTF, but you will need to generate the bindings locally. The easiest way to do so is to use the [`provider add` command](https://developer.hashicorp.com/terraform/cdktf/cli-reference/commands#provider-add), optionally with the `--force-local` flag enabled:

`cdktf provider add hashicorp/oraclepaas --force-local`

For more information and additional examples, check out our documentation on [generating provider bindings manually](https://cdk.tf/imports).

## Deprecated Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-oraclepaas](https://www.npmjs.com/package/@cdktf/provider-oraclepaas).

`npm install @cdktf/provider-oraclepaas`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-oraclepaas](https://pypi.org/project/cdktf-cdktf-provider-oraclepaas).

`pipenv install cdktf-cdktf-provider-oraclepaas`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Oraclepaas](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Oraclepaas).

`dotnet add package HashiCorp.Cdktf.Providers.Oraclepaas`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-oraclepaas](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-oraclepaas).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-oraclepaas</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-oraclepaas-go`](https://github.com/cdktf/cdktf-provider-oraclepaas-go) package.

`go get github.com/cdktf/cdktf-provider-oraclepaas-go/oraclepaas`

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-oraclepaas).
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
    "application_container",
    "data_oraclepaas_database_service_instance",
    "database_access_rule",
    "database_service_instance",
    "java_access_rule",
    "java_service_instance",
    "mysql_access_rule",
    "mysql_service_instance",
    "provider",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import application_container
from . import data_oraclepaas_database_service_instance
from . import database_access_rule
from . import database_service_instance
from . import java_access_rule
from . import java_service_instance
from . import mysql_access_rule
from . import mysql_service_instance
from . import provider
