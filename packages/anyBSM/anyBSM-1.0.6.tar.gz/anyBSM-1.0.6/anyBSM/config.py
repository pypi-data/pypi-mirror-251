from os import path
import os
import yaml
import appdirs
import logging
from typing import Union
import git

logging.basicConfig(format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

UPSTREAM = 'https://gitlab.com/anybsm/anybsm_models.git'

def get_config(ask: bool = True) -> dict:
    """Read configuration file and return its contents
    The directory containing the `anyBSM_config.yaml` file can be specified
    using the environment variable `anyBSM_CONF_DIR`. If it is not set,
    the location is determined automatically using `appdirs.user_config_dir('anyBSM')` i.e. most likely
    `~/.config/anyBSM` under Linux/Unix and
    ` ~/Library/Application Support/anyBSM` under Mac OS.
    """
    config_dir = os.environ.get('anyBSM_CONF_DIR', appdirs.user_config_dir('anyBSM'))
    config_file = path.join(config_dir, 'anyBSM_config.yaml')
    if not path.isfile(config_file):
        create_user_config(config_file, models_dir = None, ask = ask)
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        if 'models_dir' not in config:
            logger.error(f"Invaild config file: {config_file}. Variable 'models_dir' not found.")
        return config

def create_user_config(config_file: str, models_dir: Union[None, str] = None, ask: bool = False):
    """Create the user's config file and ask for path to model directory.

    Args:
        config_file: location of the config file `anyBSM_config.yaml`.
        models_dir: path to directory where models should be stored. If None, user is asked or default directory is chosen.
        ask: whether to query the user for a directory
    """
    # setup directory for model files
    config_dir = os.path.dirname(config_file)
    default_models_dir = path.join(config_dir, 'models')
    if models_dir is None:
        if ask:
            models_dir = input(f"Enter path to directory where model files should be stored (press enter for default: {default_models_dir}):") or default_models_dir
        else:
            models_dir = default_models_dir
    models_dir = os.path.expanduser(models_dir)
    if not path.exists(models_dir):
        os.makedirs(models_dir)
    else:
        if not path.isdir(models_dir):
            raise NotADirectoryError(models_dir)
    logger.info(f"storing model files at: {models_dir}")
    # download models if dir is empty
    if not os.listdir(models_dir):
        download_models(models_dir)
    # save config
    config = {}
    config['models_dir'] = models_dir
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    logger.info(f"storing config file at: {config_file}")

def download_models(models_dir: str):
    """ Clone model files from git repo

    Args:
        models_dir: download target path
    """
    if not path.isdir(models_dir):
        raise NotADirectoryError(models_dir)
    logger.info(f"Trying to download model files from {UPSTREAM}...")
    try:
        git.Repo.clone_from(UPSTREAM, models_dir)
    except Exception as e:
        logger.warning(f'Failed to clone model files. Error was:\n{e}')
    logger.info(f"Trying to download model files from {UPSTREAM}... done.")
