#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" GCP Variables """

from regscale.core.app.utils.variables import RsVariableType, RsVariablesMeta


class GcpVariables(metaclass=RsVariablesMeta):
    """
    GCP Variables class to define class-level attributes with type annotations and examples
    """

    # Define class-level attributes with type annotations and examples
    gcpProjectId: RsVariableType(str, "000000000000")
    gcpCredentials: RsVariableType(str, "path/to/credentials.json")  # noqa: F821
    # gcpOrganizationId: RsVariableTypeWithExample(str, "000000000000", required=False)
