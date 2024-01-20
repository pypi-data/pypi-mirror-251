#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOG = logging.getLogger("coodeer")

import click

from coodeer.configuration.coodeer import CoodeerSettings
from coodeer.controller.repository import RepositoryControl

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
)

pass_client = click.make_pass_decorator(RepositoryControl, ensure=True)

cfg_defaults = CoodeerSettings()


@click.group()
@click.option(
    "--bucket",
    show_default=True,
    default=cfg_defaults.bucket,
    help="Source Bucket",
)
@click.pass_context
def cli(ctx, **kwargs):
    ctx.obj = RepositoryControl(kwargs["bucket"])


@cli.command("upload", context_settings=CONTEXT_SETTINGS)
@pass_client
@click.argument("packages", nargs=-1)
def coodeer_upload(ctx, **kwargs):
    """
    Upload debian packages to source bucket
    """
    whitelisted_content_types = [
        "application/vnd.debian.binary-package",
        "application/pgp-signature",
    ]

    for path in kwargs["packages"]:
        try:
            ctx.upload(
                path, whitelisted_content_types=whitelisted_content_types
            )
        except Exception as exc:
            LOG.error(exc)
            sys.exit(1)

    sys.exit(0)


@cli.command("create", context_settings=CONTEXT_SETTINGS)
@pass_client
@click.option(
    "repository_specification",
    "--repository-specification",
    help="Repository specification file (YAML)",
)
@click.argument("repositories_root")
def coodeer_create(ctx, **kwargs):
    """
    Create local repositories
    """
    repositories_root = kwargs["repositories_root"]

    if not os.path.isdir(repositories_root):
        try:
            os.makedirs(repositories_root)
        except Exception as exc:
            LOG.error(exc)
            sys.exit(4)

    if not kwargs.get("repository_specification"):
        try:
            repository_specification = ctx.get_latest_repository_specification(
                repositories_root
            )
        except KeyError:
            LOG.error("No repository specification available!")
            sys.exit(3)
    else:
        repository_specification = kwargs.get("repository_specification")

    try:
        ctx.mk_repositories(repositories_root, repository_specification)
    except Exception as exc:
        LOG.error(exc)
        sys.exit(1)

    sys.exit(0)


@cli.command("publish", context_settings=CONTEXT_SETTINGS)
@pass_client
@click.argument(
    "repository_specification"
)
def coodeer_publish(ctx, **kwargs):
    """
    Publish repository specification
    """
    repository_specification = kwargs.get("repository_specification")

    try:
        ctx.put_latest_repository_specification(repository_specification)
    except ValueError as vexc:
        LOG.error(vexc)
        sys.exit(2)
    except Exception as vexc:
        LOG.error(vexc)
        sys.exit(1)

    sys.exit(0)
