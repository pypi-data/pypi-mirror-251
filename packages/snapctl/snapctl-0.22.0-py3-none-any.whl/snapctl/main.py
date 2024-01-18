"""
    SnapCTL entrypoint
"""
import configparser
import os
from sys import platform
from typing import Union, Callable
import typer

from snapctl.commands.byosnap import ByoSnap
from snapctl.commands.byogs import ByoGs
from snapctl.commands.snapend import Snapend
from snapctl.config.constants import API_KEY, CONFIG_FILE_MAC, CONFIG_FILE_WIN, DEFAULT_PROFILE, \
    VERSION, SNAPCTL_SUCCESS, SNAPCTL_ERROR
from snapctl.config.endpoints import END_POINTS
from snapctl.config.hashes import CLIENT_SDK_TYPES, SERVER_SDK_TYPES, PROTOS_TYPES, SERVICE_IDS
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success, info

app = typer.Typer()

######### HELPER METHODS #########


def extract_api_key(profile: str | None = None) -> str:
    """
      Extracts the API Key from the
    """
    # Parse the config
    config = configparser.ConfigParser()
    if platform == 'win32':
        config.read(os.path.expandvars(CONFIG_FILE_WIN), encoding="utf-8-sig")
    else:
        config.read(os.path.expanduser(CONFIG_FILE_MAC))
    config_profile: str = DEFAULT_PROFILE
    if profile is not None and profile != '' and profile != DEFAULT_PROFILE:
        config_profile = f'profile {profile}'
        info(f"Using Profile from input {profile}")
    else:
        env_api_key = os.getenv(API_KEY)
        if env_api_key is not None:
            config_profile = f'profile {env_api_key}'
            info(f"Using Profile environment variable {profile}")
    return config.get(config_profile, API_KEY, fallback=None, raw=True)


def get_base_url(api_key: str) -> str:
    """
        Returns the base url based on the api_key
    """
    if api_key.startswith('dev_'):
        return END_POINTS['DEV']
    if api_key.startswith('playtest_'):
        return END_POINTS['PLAYTEST']
    return END_POINTS['PROD']

######### CALLBACKS #########


def set_context_callback(ctx: typer.Context, profile: str | None = None):
    """
      Sets the context for the command
      This method will always set the context for the default profile
      Then if the command has a --profile override it will apply it
    """
    # Ensure ctx object is instantiated
    ctx.ensure_object(dict)

    # If the user has not overridden the profile you can early exit
    # this is because when you come here from `def common` the context
    # setup happens considering the default profile
    # So only if the user has overridden the profile is when we want to run this
    # method again
    if 'profile' in ctx.obj and ctx.obj['profile'] == profile:
        return

    # Extract the api_key
    api_key = extract_api_key(profile)
    if api_key is None:
        if profile is not None and profile != '':
            conf_file = ''
            if platform == 'win32':
                conf_file = os.path.expandvars(CONFIG_FILE_WIN)
            else:
                conf_file = os.path.expanduser(CONFIG_FILE_MAC)
            error(
                'Invalid profile. Please check your snap config file '
                f'at {conf_file} and try again.'
            )
        else:
            error(
                'API Key not found. Please generate a new one from the Snapser dashboard.'
            )
        raise typer.Exit(SNAPCTL_ERROR)
    # Set the context
    ctx.obj['version'] = VERSION
    ctx.obj['api_key'] = api_key
    ctx.obj['profile'] = profile if profile else DEFAULT_PROFILE
    ctx.obj['base_url'] = get_base_url(api_key)


# Presently in typer this is the only way we can expose the `--version`
def version_callback(value: bool = True):
    """
        Prints the version and exits
    """
    if value:
        success(f"Snapctl version: {VERSION}")
        raise typer.Exit(SNAPCTL_SUCCESS)


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version",
        help="Get the Snapctl version.",
        callback=version_callback
    )
):
    """
    Snapser CLI Tool
    """
    # Verify if the user has a config
    # Note this executes only when the user runs a command and not for --help or --version
    if platform == 'win32':
        config_file_path = os.path.expandvars(CONFIG_FILE_WIN)
    else:
        config_file_path = os.path.expanduser(CONFIG_FILE_MAC)
    if not os.path.isfile(config_file_path):
        error(f'Snapser configuration file not found at {config_file_path} ')
        raise typer.Exit(SNAPCTL_ERROR)
    # Set the main context this always sets the default context
    set_context_callback(ctx)

######### TYPER COMMANDS #########


@app.command()
def validate(
    profile: str = typer.Option(
        None, "--profile", help="Profile to use.", callback=set_context_callback),
):
    """
    Validate your Snapctl setup
    """
    success("Setup is valid")


@app.command()
def byosnap(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="BYOSnap Subcommands: " + ", ".join(ByoSnap.SUBCOMMANDS) + "."
    ),
    sid: str = typer.Argument(..., help="Snap Id. Should start with byosnap-"),
    # create
    name: str = typer.Option(
        None, "--name", help="(req: create) Name for your snap."
    ),
    desc: str = typer.Option(
        None, "--desc", help="(req: create) Description for your snap"
    ),
    platform_type: str = typer.Option(
        None, "--platform",
        help="(req: create) Platform for your snap - " + \
        ", ".join(ByoSnap.PLATFORMS) + "."
    ),
    language: str = typer.Option(
        None, "--language",
        help="(req: create) Language of your snap - " + \
        ", ".join(ByoSnap.LANGUAGES) + "."
    ),
    # publish-image and publish-version
    tag: str = typer.Option(
        None, "--tag", help="(req: publish-image and publish-version) Tag for your snap"
    ),
    # publish-image
    path: Union[str, None] = typer.Option(
        None, "--path", help="(req: publish-image) Path to your snap code"
    ),
    docker_file: str = typer.Option(
        "Dockerfile", help="Dockerfile name to use"
    ),
    # publish-version
    prefix: str = typer.Option(
        '/v1', "--prefix", help="(req: publish-version) URL Prefix for your snap"
    ),
    version: Union[str, None] = typer.Option(
        None, "--version",
        help="(req: publish-version) Snap version. Should start with v. Example vX.X.X"
    ),
    http_port: Union[str, None] = typer.Option(
        None, "--http-port", help="(req: publish-version) Ingress HTTP port version"
    ),
    # profile override
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=set_context_callback
    ),
) -> None:
    """
      Bring your own snap commands
    """
    # token = get_composite_token(ctx.obj['base_url'], ctx.obj['api_key'],
    # ctx.command.name, {'service_id': sid})
    byosnap_obj: ByoSnap = ByoSnap(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'], sid,
        name, desc, platform_type, language, tag, path, docker_file,
        prefix, version, http_port
    )
    validate_input_response: ResponseType = byosnap_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(byosnap_obj, command_method)
    if not method():
        error(f"BYOSnap {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"BYOSnap {subcommand} complete")


@app.command()
def byogs(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="BYOGs Subcommands: " + ", ".join(ByoGs.SUBCOMMANDS) + "."
    ),
    sid: str = typer.Argument(
        ...,  help="Game Server Id. Should start with byogs-"
    ),
    # create
    name: str = typer.Option(
        None, "--name", help="(req: create) Name for your snap"
    ),
    desc: str = typer.Option(
        None, "--desc", help="(req: create) Description for your snap"
    ),
    platform_type: str = typer.Option(
        None, "--platform",
        help="(req: create) Platform for your snap - " + \
        ", ".join(ByoGs.PLATFORMS) + "."
    ),
    language: str = typer.Option(
        None, "--language",
        help="(req: create) Language of your snap - " + \
        ", ".join(ByoGs.LANGUAGES) + "."
    ),
    # publish-image and publish-version
    tag: str = typer.Option(
        None, "--tag", help="(req: publish-image and publish-version) Tag for your snap"
    ),
    # publish-image
    path: Union[str, None] = typer.Option(
        None, "--path", help="(req: publish-image, upload-docs) Path to your snap code"
    ),
    docker_file: str = typer.Option(
        "Dockerfile", help="Dockerfile name to use"
    ),
    # publish-version
    version: Union[str, None] = typer.Option(
        None, "--version", help="(req: publish-version) Snap version"
    ),
    http_port: Union[str, None] = typer.Option(
        None, "--http-port", help="(req: publish-version) Ingress HTTP port version"
    ),
    debug_port: Union[str, None] = typer.Option(
        None, "--debug-port", help="(optional: publish-version) Debug HTTP port version"
    ),
    # profile override
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=set_context_callback
    ),
) -> None:
    """
      Bring your own game server commands
    """
    byogs_obj: ByoGs = ByoGs(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'], sid,
        name, desc, platform_type, language, tag, path, docker_file,
        version, http_port, debug_port
    )
    validate_input_response: ResponseType = byogs_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(byogs_obj, command_method)
    if not method():
        error(f"BYOGs {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"BYOGs {subcommand} complete")


@app.command()
def snapend(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="Snapend Subcommands: " + ", ".join(Snapend.SUBCOMMANDS) + "."
    ),
    snapend_id: str = typer.Argument(..., help="Snapend Id"),
    # download
    category: str = typer.Option(
        None, "--category",
        help=(
            "(req: download) Category of the Download: " +
            ", ".join(Snapend.DOWNLOAD_CATEGORY) + "."
        )
    ),
    path: Union[str, None] = typer.Option(
        None, "--path", help="(req: download) Path to save the SDK"),
    platform_type: str = typer.Option(
        None, "--type",
        help=(
            "(req: --category client-sdk|server-sdk|protos --type ) "
            "SDK Types: client-sdk(" + ", ".join(CLIENT_SDK_TYPES.keys()) +
            ") server-sdk(" + ", ".join(SERVER_SDK_TYPES.keys()) +
            ") protos(" + ", ".join(PROTOS_TYPES.keys()) + ")"
        )
    ),
    auth_type: str = typer.Option(
        'user', "--auth-type",
        help=(
            "(optional: download) Only applicable for --category server-sdk --auth-type"
            "Auth-Types: ()" + ", ".join(Snapend.AUTH_TYPES) + ")"
        )
    ),
    snaps: Union[str, None] = typer.Option(
        None, "--snaps",
        help=(
            "(optional: download) Comma separated list of snap ids to customize the "
              "SDKs, protos or admin settings. "
              "snaps(" + ", ".join(SERVICE_IDS)
        )
    ),
    # update
    byosnaps: str = typer.Option(
        None, "--byosnaps",
        help=(
            "(optional: update) Comma separated list of BYOSnap ids and versions. "
            "Eg: service-1:v1.0.0,service-2:v1.0.0"
        )
    ),
    byogs: str = typer.Option(
        None, "--byogs",
        help=(
            "(optional: update) Comma separated list of BYOGs fleet name, ids and versions. "
            "Eg: fleet-1:service-1:v1.0.0,fleet-2:service-2:v1.0.0"
        )
    ),
    blocking: bool = typer.Option(
        False, "--blocking",
        help=(
            "(optional: update) Set to true if you want to wait for the update to complete "
            "before returning."
        )
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=set_context_callback
    ),
) -> None:
    """
      Snapend commands
    """
    snapend_obj: Snapend = Snapend(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'],
        snapend_id, category, platform_type, auth_type,
        path, snaps, byosnaps, byogs, blocking
    )
    validate_input_response: ResponseType = snapend_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(snapend_obj, command_method)
    if not method():
        error(f"Snapend {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"Snapend {subcommand} complete")
