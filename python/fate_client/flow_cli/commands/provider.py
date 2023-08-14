#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import click

from ..utils import cli_args
from ..utils.cli_utils import prettify, preprocess
from fate_client.flow_sdk import FlowClient


@click.group(short_help="Permission Operations")
@click.pass_context
def provider(ctx):
    """
    \b
    Provides numbers of data operational commands, including upload, download and etc.
    For more details, please check out the help text.
    """
    pass


@provider.command("register", short_help="Register New Provider Command")
@cli_args.CONF_PATH
@click.pass_context
def register(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow provider register -c /data/project/xxx.json
    """
    config_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.provider.register(**config_data)
    prettify(response)


@provider.command("query", short_help="query Provider Command")
@cli_args.NAME
@cli_args.DEVICE
@cli_args.VERSION
@cli_args.PROVIDER_NAME
@click.pass_context
def query(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow provider query --name xxx
    """
    client: FlowClient = ctx.obj["client"]
    response = client.provider.query(**kwargs)
    prettify(response)


@provider.command("delete", short_help="delete Provider Command")
# @cli_args.NAME
# @cli_args.DEVICE
# @cli_args.VERSION
# @cli_args.PROVIDER_NAME
@cli_args.CONF_PATH
@click.pass_context
def delete(ctx, **kwargs):
    """
    - DESCRIPTION:


    \b
    - USAGE:
        flow provider delete -c /data/project/xxx.json
    """
    config_data = preprocess(**kwargs)
    client: FlowClient = ctx.obj["client"]
    response = client.provider.delete(**config_data)
    prettify(response)





