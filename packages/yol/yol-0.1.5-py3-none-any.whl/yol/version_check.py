import requests
import pkg_resources
import os
from datetime import datetime, timedelta
from .version import __version__, __release_date__

def get_current_version_and_date():
    return "yol", __version__, datetime.strptime(__release_date__, '%Y-%m-%d')

def get_latest_version_from_pypi(package_name):
    try:
        response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
        if response.status_code == 200:
            data = response.json()
            return data['info']['version']
    except requests.RequestException:
        return None


def check_for_update():
    package_name, current_version, CURRENT_VERSION_DATE = get_current_version_and_date()
    if not current_version:
        return "Unable to determine current version"

    latest_version = get_latest_version_from_pypi(package_name)
    if latest_version and latest_version != current_version:
        return latest_version
    else:
        if datetime.now() > CURRENT_VERSION_DATE + timedelta(days=30):
            return 'version check failed, consider updating'
    return None

# Use this function to trigger the version check
update_version = check_for_update()
