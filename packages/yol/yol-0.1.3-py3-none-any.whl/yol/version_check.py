import requests
import pkg_resources
from configparser import ConfigParser
import os
from datetime import datetime, timedelta

def get_current_version_and_date():
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), '../setup.cfg'))
    package_name = config['metadata']['name']
    current_version = config['metadata']['version']
    
    # Parse the release date from the setup.cfg if present
    release_date_str = config['metadata'].get('release_date', None)
    release_date = datetime.strptime(release_date_str, '%Y-%m-%d') if release_date_str else None
    
    return package_name, current_version, release_date

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
