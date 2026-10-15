"""Non-secret runtime inventory; suitable for the exact base and its overlay."""
import hashlib
from importlib import metadata
import json
import os
from pathlib import Path
import sys


FEATURES = [
    'jupyterlab-git', 'nbgitpuller', 'jupyter-resource-usage',
    'catppuccin-jupyterlab', 'jupyterlab-horizon-theme',
    'jupyter-server-proxy', 'jupyter-glances-proxy',
    'notebook-intelligence', 'git-credential-helpers',
]


def inventory():
    files = {}
    for name in FEATURES:
        dist = metadata.distribution(name)
        for item in dist.files or ():
            path = dist.locate_file(item)
            if path.is_file() and '__pycache__' not in path.parts:
                files[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    # These files are part of the inherited image startup/config contract.
    for root in ['/etc/jupyter', '/usr/local/etc/jupyter',
                 str(Path(sys.prefix) / 'etc/jupyter'), '/usr/local/bin']:
        for path in Path(root).rglob('*'):
            if path.is_file() and (root != '/usr/local/bin' or path.name in {
                'start.sh', 'start-notebook.py', 'start-singleuser.py',
            }):
                files[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        'python': sys.version.split()[0], 'prefix': sys.prefix,
        'uid': os.getuid(), 'gid': os.getgid(), 'cwd': os.getcwd(),
        'versions': {d.metadata['Name'].lower().replace('_', '-'): d.version
                     for d in metadata.distributions()},
        'feature_files': files,
    }


if __name__ == '__main__':
    print(json.dumps(inventory(), sort_keys=True, indent=2))
