from dataclasses import dataclass
import importlib
import logging
import os
from packaging.requirements import Requirement
from pathlib import Path
import sys
from typing import Dict, Any, Optional, List

from envzy import AutoExplorer, ModulePathsList

from datasphere.config import PythonEnv as PythonEnvConfig
import yaml

logger = logging.getLogger(__name__)


@dataclass
class PythonEnv:
    version: str
    local_modules_paths: ModulePathsList
    requirements: List[str]
    pip_options: Optional[PythonEnvConfig.PipOptions] = None

    @property
    def conda_yaml(self) -> str:
        dependencies = [f'python=={self.version}', 'pip']

        requirements = list(self.requirements)  # copy
        if requirements:
            if self.pip_options:
                # Requirements from envzy explorer only contains precise packages versions.
                # User-defined requirements can contain anything supported by pip, so clash with `pip-options`
                # is possible (not solved by now).
                if self.pip_options.extra_index_urls:
                    requirements = [f'--extra-index-url {url}' for url in self.pip_options.extra_index_urls] + \
                                   requirements
                if self.pip_options.no_deps:
                    requirements = ['--no-deps'] + requirements
            dependencies.append({'pip': requirements})

        return yaml.dump({'name': 'default', 'dependencies': dependencies}, sort_keys=False)


def define_py_env(main_script_path: str, py_env_cfg: PythonEnvConfig) -> PythonEnv:
    version = None
    local_modules_paths = None
    requirements = None

    if not py_env_cfg.is_fully_manual:
        # User may not add cwd to PYTHONPATH, in case of running execution through `datasphere`, not `python -m`.
        # Since path to python script can be only relative, this should always work.
        sys.path.append(os.getcwd())
        namespace = _get_module_namespace(main_script_path)
        extra_index_urls = []
        if py_env_cfg.pip_options and py_env_cfg.pip_options.extra_index_urls:
            extra_index_urls = py_env_cfg.pip_options.extra_index_urls
        explorer = AutoExplorer(extra_index_urls=extra_index_urls)

        version = '.'.join(str(x) for x in explorer.target_python)
        local_modules_paths = explorer.get_local_module_paths(namespace)
        requirements = [
            (f'{name}=={version}' if version else name) for name, version in
            explorer.get_pypi_packages(namespace).items()
        ]

        logger.debug('auto-defined python env:\n\tversion: %s\n\tpypi packages: %s\n\trequirements: %s',
                     version, local_modules_paths, requirements)

    return PythonEnv(
        version=py_env_cfg.version if py_env_cfg.version else version,
        requirements=_parse_requirements(py_env_cfg.requirements) if py_env_cfg.requirements else requirements,
        local_modules_paths=py_env_cfg.local_modules_paths if py_env_cfg.local_modules_paths else local_modules_paths,
        pip_options=py_env_cfg.pip_options,
    )


def _get_module_namespace(path: str) -> Dict[str, Any]:
    module_spec = importlib.util.spec_from_file_location('module', path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return vars(module)


# Allow packages specifiers (with extras) and flags/options (supported by server).
def _parse_requirements(f: Path) -> List[str]:
    lines = [line.strip() for line in f.read_text().strip().split('\n') if line.strip()]
    for line in lines:
        if line == '--no-deps':
            continue
        if line.startswith('--extra-index-url'):
            continue
        req = Requirement(line)
        assert req.marker is None, f'requirement markers are not supported ({line})'
        assert req.url is None, f'requirement url is not supported ({line})'
    return lines
