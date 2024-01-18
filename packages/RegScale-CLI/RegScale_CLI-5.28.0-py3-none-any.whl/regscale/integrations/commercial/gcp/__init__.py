#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" RegScale GCP Package """

import click
from .findings import sync_gcp_findings
from .assets import sync_gcp_assets


@click.group()
def gcp():
    """GCP Integrations"""


@gcp.command(name="sync_findings")
@click.option(
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
def sync_findings(regscale_ssp_id):
    """Sync GCP Findings to RegScale."""
    sync_gcp_findings(plan_id=regscale_ssp_id)


@gcp.command(name="sync_assets")
@click.option(
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
def sync_assets(regscale_ssp_id):
    """Sync GCP Assets to RegScale."""
    sync_gcp_assets(plan_id=regscale_ssp_id)
