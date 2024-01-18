"""
  Snapend CLI commands
"""
from sys import platform
from typing import Union

import os
import time
import requests
from requests.exceptions import RequestException

from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.config.constants import SERVER_CALL_TIMEOUT
from snapctl.config.hashes import CLIENT_SDK_TYPES, SERVER_SDK_TYPES, PROTOS_TYPES
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success, info


class Snapend:
    """
      CLI commands exposed for a Snapend
    """
    SUBCOMMANDS = ['download', 'update', 'state']
    DOWNLOAD_CATEGORY = [
        'client-sdk', 'server-sdk', 'protos', 'admin-settings'
    ]
    DOWNLOAD_TYPE_NOT_REQUIRED = ['admin-settings']
    AUTH_TYPES = ['user', 'app']
    BLOCKING_CALL_SLEEP = 5
    MAX_BLOCKING_RETRIES = 24

    def __init__(
        self, subcommand: str, base_url: str, api_key: str, snapend_id: str, category: str,
        platform_type: str, auth_type: str,  path: Union[str, None], snaps: Union[str, None],
        byosnaps: Union[str, None], byogs: Union[str, None], blocking: bool = False
    ) -> None:
        self.subcommand: str = subcommand
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.snapend_id: str = snapend_id
        self.category: str = category
        self.download_types: Union[
            dict[str, dict[str, str]], None
        ] = Snapend._make_download_type(category)
        self.auth_type: str = auth_type
        self.platform_type: str = platform_type
        self.path: Union[str, None] = path
        self.snaps: Union[str, None] = snaps
        self.byosnap_list: Union[list, None] = Snapend._make_byosnap_list(
            byosnaps) if byosnaps else None
        self.byogs_list: Union[str, None] = Snapend._make_byogs_list(
            byogs) if byogs else None
        self.blocking: bool = blocking

    @staticmethod
    def _make_download_type(category: str):
        if category == 'client-sdk':
            return CLIENT_SDK_TYPES
        if category == 'server-sdk':
            return SERVER_SDK_TYPES
        if category == 'protos':
            return PROTOS_TYPES
        return None

    @staticmethod
    def _make_byosnap_list(byosnaps: str) -> list:
        byosnap_list = []
        for byosnap in byosnaps.split(','):
            byosnap = byosnap.strip()
            if len(byosnap.split(':')) != 2:
                return []
            byosnap_list.append({
                'service_id': byosnap.split(':')[0],
                'service_version': byosnap.split(':')[1]
            })
        return byosnap_list

    @staticmethod
    def _make_byogs_list(byogs: str) -> list:
        byogs_list = []
        for byog in byogs.split(','):
            byog = byog.strip()
            if len(byog.split(':')) != 3:
                return []
            byogs_list.append({
                'fleet_name': byog.split(':')[0],
                'service_id': byog.split(':')[1],
                'service_version': byog.split(':')[2]
            })
        return byogs_list

    def _get_snapend_state(self) -> str:
        try:
            url = f"{self.base_url}/v1/snapser-api/snapends/{self.snapend_id}"
            res = requests.get(
                url, headers={'api-key': self.api_key}, timeout=SERVER_CALL_TIMEOUT
            )
            cluster_object = res.json()
            if 'cluster' in cluster_object and 'id' in cluster_object['cluster'] and \
                    cluster_object['cluster']['id'] == self.snapend_id and \
                    'state' in cluster_object['cluster']:
                return cluster_object['cluster']['state']
        except RequestException as e:
            error(f"Exception: Unable to get Snapend state {e}")
        return 'INVALID'

    def _blocking_get_status(self) -> bool:
        total_tries = 0
        while True:
            total_tries += 1
            if total_tries > Snapend.MAX_BLOCKING_RETRIES:
                error("Going past maximum tries. Exiting...")
                return False
            current_state = self._get_snapend_state()
            if current_state == 'INVALID':
                error("Unable to get the snapend state. Exiting...")
                return False
            if current_state == 'LIVE':
                success('Updated your snapend. Your snapend is Live.')
                return True
            info(f'Current snapend state is {current_state}')
            info(f"Retrying in {Snapend.BLOCKING_CALL_SLEEP} seconds...")
            time.sleep(Snapend.BLOCKING_CALL_SLEEP)

    def validate_input(self) -> ResponseType:
        """
          Validator
        """
        response: ResponseType = {
            'error': True,
            'msg': '',
            'data': []
        }
        # Check subcommand
        if not self.subcommand in Snapend.SUBCOMMANDS:
            response['msg'] = \
                f"Invalid command. Valid commands are {', '.join(Snapend.SUBCOMMANDS)}."
            return response
        # Check sdk-download commands
        if self.subcommand == 'download':
            if self.category not in Snapend.DOWNLOAD_CATEGORY:
                response['msg'] = (
                    "Invalid SDK category. Valid categories are "
                    f"{', '.join(Snapend.DOWNLOAD_CATEGORY)}."
                )
                return response
            if self.category not in Snapend.DOWNLOAD_TYPE_NOT_REQUIRED and \
                    (self.download_types is None or self.platform_type not in self.download_types):
                response['msg'] = "Invalid Download type."
                return response
            # Check file path
            if self.path and not os.path.isdir(f"{self.path}"):
                response['msg'] = (
                    f"Invalid path {self.path}. "
                    "Please enter a valid path to save your SDK"
                )
                return response
            # Check the auth type
            if self.category == 'server-sdk' and self.auth_type not in Snapend.AUTH_TYPES:
                response['msg'] = (
                    "Invalid auth type. Valid auth types are "
                    f"{', '.join(Snapend.AUTH_TYPES)}."
                )
                return response
        # Check update commands
        elif self.subcommand == 'update':
            byosnap_present = True
            if self.byosnap_list is None or len(self.byosnap_list) == 0:
                byosnap_present = False
            byogs_present = True
            if self.byogs_list is None or len(self.byogs_list) == 0:
                byogs_present = False
            if not byosnap_present and not byogs_present:
                response['msg'] = "The update command needs one of byosnaps or byogs"
                return response
        # Send success
        response['error'] = False
        return response

    def download(self) -> bool:
        """
          Download SDKs, Protos and Admin Settings
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description=f'Downloading your Custom {self.category}...', total=None)
            try:
                url = (
                    f"{self.base_url}/v1/snapser-api/snapends/{self.snapend_id}/"
                    f"download?category={self.category}"
                )
                if self.category not in Snapend.DOWNLOAD_TYPE_NOT_REQUIRED:
                    url += (
                        f"&type={self.download_types[self.platform_type]['type']}"
                        f"&subtype={self.download_types[self.platform_type]['subtype']}"
                    )
                url_auth_type: str = 'user'
                if self.category == 'server-sdk' and self.auth_type == 'app':
                    url_auth_type = 'app'
                url += f"&auth_type={url_auth_type}"
                if self.snaps:
                    url += f"&snaps={self.snaps}"
                res = requests.get(
                    url, headers={'api-key': self.api_key}, timeout=SERVER_CALL_TIMEOUT
                )
                fn: str = f"snapser-{self.snapend_id}-admin-settings.json"
                if self.category != 'admin-settings':
                    fn = f"snapser-{self.snapend_id}-{self.category}-{self.platform_type}-{self.auth_type}.zip"
                file_path_symbol = '/'
                if platform == 'win32':
                    file_path_symbol = '\\'
                if self.path is not None:
                    sdk_save_path = f"{self.path}{file_path_symbol}{fn}"
                else:
                    sdk_save_path = f"{os.getcwd()}{file_path_symbol}{fn}"
                if res.ok:
                    with open(sdk_save_path, "wb") as file:
                        file.write(res.content)
                    success(f"SDK saved at {sdk_save_path}")
                    return True
                error('Unable to download your custom SDK')
            except RequestException as e:
                error(f"Exception: Unable to download the SDK {e}")
            return False

    def update(self) -> bool:
        """
          Update a Snapend
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Updating your Snapend...', total=None)
            try:
                payload = {
                    'byosnap_updates': self.byosnap_list,
                    'byogs_updates': self.byogs_list
                }
                url = f"{self.base_url}/v1/snapser-api/snapends/{self.snapend_id}"
                res = requests.patch(
                    url, json=payload, headers={'api-key': self.api_key},
                    timeout=SERVER_CALL_TIMEOUT
                )
                if res.ok:
                    if self.blocking:
                        return self._blocking_get_status()
                    success(
                        'Snapend update has been initiated. '
                        'You can check the status using `snapctl snapend state`'
                    )
                    return True
                response_json = res.json()
                error(response_json['details'][0])
            except RequestException as e:
                error(f"Exception: Unable to update your snapend {e}")
            return False

    def state(self) -> bool:
        """
          Get the state of a Snapend
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description='Getting your Snapend state...', total=None)
            current_state = self._get_snapend_state()
            if current_state != 'INVALID':
                success('Current snapend state is: ' + current_state)
                return True
            error("Unable to get the snapend state.")
            return False
