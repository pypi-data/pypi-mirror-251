import argparse
import dataclasses
import logging
import os
from typing import Dict, List, Optional

from dotenv import dotenv_values

from .addons_installer import AddonsFinder, AddonsInstaller
from .api import OdooAddonsDef
from .git_credential import GitCredentialManager

_logger = logging.getLogger("install_addons")


@dataclasses.dataclass
class ArgsCli:
    profiles: Optional[str] = dataclasses.field(default=None)
    install: Optional[str] = dataclasses.field(default=None)
    all: bool = dataclasses.field(default=False)
    cmd_only: bool = dataclasses.field(default=False)


def install_from_env(args: ArgsCli = None) -> Optional[List[List[str]]]:
    """Entrypoint for the CLI"""
    if not args:
        args: ArgsCli = _get_parser().parse_args(namespace=ArgsCli())

    if not args.install:
        args.all = True  # default to --all, if both are present --all will override
    env_vars = dict(os.environ)
    if args.profiles:
        env_vars.update(_load_profiles(_get_profiles(args.profiles)))
    specifics_addons = args.install and _get_addons(args.install) or []
    cmd = _install_addons(args, env_vars, specifics_addons)
    return cmd if args.cmd_only else None


def _install_addons(args: ArgsCli, env_vars: Dict[str, str], specifics_addons: List[str]) -> [List[List[str]]]:
    addons: List[OdooAddonsDef] = AddonsFinder().parse_env(env_vars)
    cmd = []
    for addon in addons:
        if addon.name in specifics_addons or args.all:
            cmd.append(AddonsInstaller.install(addon, return_cmd=args.cmd_only))
    return cmd


def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--profiles", dest="profiles", help="Coma separated profile files")
    parser.add_argument(
        "-i", dest="install", help="Coma separated list of addons to install (amongst the addons present in ENV vars)"
    )
    parser.add_argument(
        "--all", dest="all", action="store_true", help="All addons in ENV variables are installed (override -i)"
    )
    parser.add_argument(
        "--cmd-only",
        dest="cmd_only",
        action="store_true",
        help="Do not perform install, returns the command to perform it",
    )
    return parser


def _get_profiles(profiles: str) -> List[str]:
    """--profiles is followed by comma separated filename"""
    return profiles.split(",")


def _get_addons(addons_arg: str) -> List[str]:
    """-i is followed by a comma separated list of addons name, we use uppercase in AddonsFinder and ENV declaration"""
    return addons_arg.upper().split(",")


def _load_profiles(profiles: List[str]) -> Dict[str, str]:
    extra_env = {}
    for profile in profiles:
        path_profile = os.path.abspath(os.path.expanduser(profile))
        if not os.path.exists(path_profile):
            _logger.info("Can't load %s, file don't exist", path_profile)
        else:
            extra_env.update(dotenv_values(path_profile))
    return extra_env


def setup_git_from_env(args: ArgsCli = None) -> Optional[List[List[str]]]:
    if not args:
        args: ArgsCli = _get_parser().parse_args(namespace=ArgsCli())

    if not args.install:
        args.all = True  # default to --all, if both are present --all will override
    env_vars = dict(os.environ)
    if args.profiles:
        env_vars.update(_load_profiles(_get_profiles(args.profiles)))
    specifics_addons = args.install and _get_addons(args.install) or []
    cmd = _cmd_setup_git(env_vars, specifics_addons, args.cmd_only)
    return cmd if args.cmd_only else None


def _cmd_setup_git(env_vars: Dict[str, str], filter: List[str], dry_run: bool = True) -> List[List[str]]:
    manager = GitCredentialManager(env_vars)
    result = []
    for extractor in manager.create_extractors():
        ad_def = extractor.extract(manager.env_vars)
        if not filter or ad_def.name not in filter:
            _logger.info("Exclude %s", ad_def.name)
            continue
        cmd: List[str] = manager.get_cmd(ad_def)
        result.append(cmd)
        if dry_run:
            _logger.info("> %s", " ".join(cmd))
            continue
        AddonsInstaller.exec_cmd(cmd, force_log=True)
    return result
