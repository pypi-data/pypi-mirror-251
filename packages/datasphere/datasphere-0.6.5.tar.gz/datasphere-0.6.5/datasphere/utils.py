import hashlib
import importlib.metadata
import logging
import re

from tabulate import tabulate
from typing import BinaryIO, List, Optional, Tuple

from envzy.pypi import PYPI_INDEX_URL_DEFAULT, get_project_page
from google.protobuf.timestamp_pb2 import Timestamp

from datasphere.api import jobs_pb2

logger = logging.getLogger(__name__)


def get_sha256_and_size(f: BinaryIO) -> Tuple[str, int]:
    h = hashlib.sha256()
    sz = 0

    for chunk in iter(lambda: f.read(65_536), b''):
        h.update(chunk)
        sz += len(chunk)

    return h.hexdigest(), sz


def format_jobs_table(jobs: List[jobs_pb2.Job]) -> str:
    def format_timestamp(ts: Optional[Timestamp]) -> str:
        if not ts or (ts.seconds == 0 and ts.nanos == 0):
            return ''
        return ts.ToDatetime().isoformat()

    def get_row(job: jobs_pb2.Job) -> list:
        return [
            job.id,
            job.name,
            job.desc,
            format_timestamp(job.created_at),
            format_timestamp(job.finished_at),
            jobs_pb2._JOBSTATUS.values_by_number[job.status].name,
            job.created_by_id,
        ]

    return tabulate(
        [get_row(job) for job in jobs],
        headers=['ID', 'Name', 'Description', 'Created at', 'Finished at', 'Status', 'Created by'],
    )


def query_yes_no(question: str, default: Optional[bool] = True) -> bool:
    prompt = {True: 'Y/n', False: 'y/N', None: 'y/n'}[default]
    options = {'yes': True, 'y': True, 'no': False, 'n': False}
    while True:
        choice = input(f'{question} [{prompt}]: ').lower()
        if default is not None and choice == '':
            return default
        elif choice in options:
            return options[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def humanize_bytes_size(size: int) -> str:
    for unit in ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'):
        if abs(size) < 1024.0:
            return f'{size:3.1f}{unit}B'
        size /= 1024.0
    return f'{size:.1f}YB'


def parse_human_size(size: str) -> int:
    size = size.strip().upper()
    if size.isdigit():
        return int(size)

    for unit, mult in [('KB', 1 << 10), ('MB', 1 << 20), ('GB', 1 << 30), ('TB', 1 << 40), ('PB', 1 << 50)]:
        if size.endswith(unit):
            size = size[:-len(unit)].strip()
            return int(size) * mult

    raise ValueError(f'Invalid size: {size}')


package = 'datasphere'
version_pattern = re.compile(r'\d+\.\d+\.\d+')


def check_package_version():
    current = importlib.metadata.version(package)

    project_page = get_project_page(pypi_index_url=PYPI_INDEX_URL_DEFAULT, name=package)

    # filter release candidates and other non-release staff
    release_packages = [p for p in project_page.packages if version_pattern.fullmatch(p.version)]

    if len(release_packages) == 0:
        logger.warning('No released packages found to check CLI version')
        return

    # latest package should be last in list, but let's sort by version lexicographically, just in case
    latest_package = sorted(release_packages, key=lambda p: p.version)[-1]
    latest = latest_package.version

    if current != latest:
        logger.warning('Installed version of CLI is %s, and the latest version is %s, please update CLI using '
                       '`pip install -U %s`', current, latest, package)
