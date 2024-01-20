'''
# CDKTF prebuilt bindings for hashicorp/googleworkspace provider version 0.7.0

HashiCorp made the decision to stop publishing new versions of prebuilt [Terraform googleworkspace provider](https://registry.terraform.io/providers/hashicorp/googleworkspace/0.7.0) bindings for [CDK for Terraform](https://cdk.tf) on January 19, 2024. As such, this repository has been archived and is no longer supported in any way by HashiCorp. Previously-published versions of this prebuilt provider will still continue to be available on their respective package managers (e.g. npm, PyPi, Maven, NuGet), but these will not be compatible with new releases of `cdktf` past `0.20.0` and are no longer eligible for commercial support.

As a reminder, you can continue to use the `hashicorp/googleworkspace` provider in your CDK for Terraform (CDKTF) projects, even with newer versions of CDKTF, but you will need to generate the bindings locally. The easiest way to do so is to use the [`provider add` command](https://developer.hashicorp.com/terraform/cdktf/cli-reference/commands#provider-add), optionally with the `--force-local` flag enabled:

`cdktf provider add hashicorp/googleworkspace --force-local`

For more information and additional examples, check out our documentation on [generating provider bindings manually](https://cdk.tf/imports).

## Deprecated Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-googleworkspace](https://www.npmjs.com/package/@cdktf/provider-googleworkspace).

`npm install @cdktf/provider-googleworkspace`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-googleworkspace](https://pypi.org/project/cdktf-cdktf-provider-googleworkspace).

`pipenv install cdktf-cdktf-provider-googleworkspace`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Googleworkspace](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Googleworkspace).

`dotnet add package HashiCorp.Cdktf.Providers.Googleworkspace`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-googleworkspace](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-googleworkspace).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-googleworkspace</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-googleworkspace-go`](https://github.com/cdktf/cdktf-provider-googleworkspace-go) package.

`go get github.com/cdktf/cdktf-provider-googleworkspace-go/googleworkspace/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-googleworkspace-go/blob/main/googleworkspace/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-googleworkspace).
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
    "chrome_policy",
    "data_googleworkspace_chrome_policy_schema",
    "data_googleworkspace_domain",
    "data_googleworkspace_domain_alias",
    "data_googleworkspace_group",
    "data_googleworkspace_group_member",
    "data_googleworkspace_group_members",
    "data_googleworkspace_group_settings",
    "data_googleworkspace_groups",
    "data_googleworkspace_org_unit",
    "data_googleworkspace_privileges",
    "data_googleworkspace_role",
    "data_googleworkspace_schema",
    "data_googleworkspace_user",
    "data_googleworkspace_users",
    "domain",
    "domain_alias",
    "gmail_send_as_alias",
    "group",
    "group_member",
    "group_members",
    "group_settings",
    "org_unit",
    "provider",
    "role",
    "role_assignment",
    "schema",
    "user",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import chrome_policy
from . import data_googleworkspace_chrome_policy_schema
from . import data_googleworkspace_domain
from . import data_googleworkspace_domain_alias
from . import data_googleworkspace_group
from . import data_googleworkspace_group_member
from . import data_googleworkspace_group_members
from . import data_googleworkspace_group_settings
from . import data_googleworkspace_groups
from . import data_googleworkspace_org_unit
from . import data_googleworkspace_privileges
from . import data_googleworkspace_role
from . import data_googleworkspace_schema
from . import data_googleworkspace_user
from . import data_googleworkspace_users
from . import domain
from . import domain_alias
from . import gmail_send_as_alias
from . import group
from . import group_member
from . import group_members
from . import group_settings
from . import org_unit
from . import provider
from . import role
from . import role_assignment
from . import schema
from . import user
