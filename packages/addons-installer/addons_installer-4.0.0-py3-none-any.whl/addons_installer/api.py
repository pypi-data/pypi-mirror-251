from __future__ import annotations

import abc
import dataclasses
import logging
import os
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar, Union

import gitman.models.config

_logger = logging.getLogger("install_addons")
_logger.setLevel(logging.INFO)


@dataclasses.dataclass
class GitManAddonsConfig:
    path: str
    name_filter: List[str] = dataclasses.field(default_factory=list)
    no_locked_sources: bool = False
    enable: bool = False


class KeySuffix(object):
    def __init__(self, addons: EnvKeyExtractor, name: str, default: str = None, have_default: bool = True):
        self.name = name
        self.prefix = addons.prefix
        self.base_key = addons.identifier
        self.default_value = default
        self.have_default = have_default

    def get_value(
        self, env_vars: Dict[str, str], *, use_default_value: bool = True, use_default_key: bool = True
    ) -> Optional[str]:
        """
        Retrieve the value in the env_vars
        Look is this order

        1. full_key in env_vars
        2. default_key in env_vars
        3. default value
        4. None

        You can change the behavior and use the default value or the default

        Args:
            env_vars: the values to look in
            use_default_value: If no value found with de full key name then the default key is used
            use_default_key: If no value with the default key or the
            full key is found then we use the static default value

        Returns: the value or the default one, otherwise None

        """
        r = env_vars.get(self.full_key, None)
        if not r and use_default_key and self.have_default:
            r = env_vars.get(self.default_key)
        if not r and use_default_value:
            r = self.default_value
        return r

    def in_env(self, env_vars: Dict[str, str], use_default_key: bool = False) -> bool:
        in_env = self.full_key in env_vars.keys()
        if not in_env and use_default_key:
            in_env = self.default_key in env_vars.keys()
        return in_env

    def _get_key(self, prefix: str, middle: str, suffix: str) -> str:
        return "_".join([s for s in [prefix, middle, suffix] if s]).upper()

    @property
    def full_key(self) -> str:
        return self._get_key(self.prefix, self.base_key, self.name)

    @property
    def default_key(self) -> Optional[str]:
        return self.have_default and self._get_key(self.prefix, AddonsSuffix.ADDONS_DEFAULT, self.name) or None

    def __repr__(self) -> str:
        return "%s(%s, default=%s)" % (type(self).__name__, self.full_key, self.default_key)


T = TypeVar("T", bound=Any)


class EnvKeyExtractor(Generic[T], abc.ABC):
    KEY_DEFAULT = "DEFAULT"
    KEY_SUFFIX_EXCLUDE = "EXCLUDE"

    def __init__(self, base_key: str, prefix: str = None):
        self.base_key = base_key
        self.prefix = prefix or ""
        self._key_registry: Dict[str, KeySuffix] = {}
        self.NAME = self.create_key("", have_default=False)

    @property
    def identifier(self) -> str:
        return self.base_key.replace(self.prefix, "").strip("_")

    def to_dict(self, env_vars: Dict[str, str]) -> Dict[KeySuffix, str]:
        return {key: key.get_value(env_vars) for key_name, key in self._key_registry.items()}

    def get_suffix_keys(self) -> List[str]:
        return list(self._key_registry.keys())

    def create_key(self, name: str, default: str = None, have_default: bool = True) -> KeySuffix:
        key = KeySuffix(addons=self, name=name, default=default, have_default=have_default)
        self._key_registry.setdefault(name, key)
        return key

    @abc.abstractmethod
    def extract(self, env_vars: Dict[str, str]) -> T:
        raise NotImplementedError()

    def is_valid(self) -> bool:
        return (
            self.base_key.startswith(self.prefix)
            and not any(self.base_key.endswith(suffix) for suffix in self.get_suffix_keys() if suffix)
            and not self.base_key.endswith(self.KEY_SUFFIX_EXCLUDE)
            and self.NAME.full_key == self.base_key
        )

    def __repr__(self) -> str:
        return "%s(%s)" % (type(self).__name__, self.identifier)

    def __eq__(self, other: AddonsSuffix) -> bool:
        return isinstance(other, AddonsSuffix) and other.identifier == self.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)


EKE_E = TypeVar("EKE_E", bound=Any)
EKE = TypeVar("EKE", bound="EnvKeyExtractor")


class ExtractorManager(Generic[EKE]):
    """
    This class try o find all the Odoo dependency Addons from Environ Var
    The Odoo Addons can be declared in 2 ways.
    ADDONS_GIT_XXX or ADDONS_LOCAL_XXX
    In case of `ADDONS_GIT_XXX` then [GitOdooAddons][GitOdooAddons] is used to discover all other necessary Key
    In case of `ADDONS_LOCAL_XXX` then [LocalODooAddons][LocalODooAddons] is used.
    All supported types are defined in `types`

    Attributes:
        type: Contains all the supported Addons Type
    """

    def __init__(self, extractor_type: Type[EKE], *, env_vars: Dict[str, str] = None):
        self.env_vars = env_vars and dict(env_vars) or {}
        self.extractor_type: Type[EKE] = extractor_type

    def create_extractors(
        self,
    ) -> List[EKE]:
        founded = {}
        for env_key in sorted(self.env_vars.keys()):
            addon = self._try_parse_key(env_key)
            if addon and self.env_vars.get(env_key) != str(False):
                _logger.info("Found depends %s from %s", addon, addon.identifier)
                founded[addon.identifier] = addon
        return list(dict.fromkeys(founded.values()).keys())

    def _try_parse_key(self, env_key: str) -> Union[EKE, None]:
        """

        :param env_key:
        :return:
        """
        addons: EnvKeyExtractor = self.extractor_type(env_key)
        if addons.is_valid():
            _logger.info("Found depends %s from %s", addons, env_key)
            return addons
        return None

    def extract(self, *extractors: EKE) -> List[EKE_E]:
        if not extractors:
            extractors = self.create_extractors()
        return [extractor.extract(self.env_vars) for extractor in extractors]


class AddonsSuffix(EnvKeyExtractor, abc.ABC):
    ADDONS_DEFAULT = EnvKeyExtractor.KEY_DEFAULT
    ADDONS_SUFFIX_EXCLUDE = EnvKeyExtractor.KEY_SUFFIX_EXCLUDE

    def __init__(self, base_key: str, prefix: str):
        super(AddonsSuffix, self).__init__(base_key, prefix)
        self.GITMAN_DISABLE = self.create_key("GITMAN_DISABLE", default=str(False))
        self.GITMAN_GROUP = self.create_key("GITMAN_GROUP")
        self.GITMAN_NO_LOCKED_SOURCES = self.create_key("GITMAN_NO_LOCKED_SOURCES", default=str(False))

    @abc.abstractmethod
    def extract(self, env_vars: Dict[str, str]) -> OdooAddonsDef:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_path(self, env_vars: Dict[str, str], res: Dict[KeySuffix, str]) -> str:
        ...

    def get_gitman_config(self, env_vars: Dict[str, str]) -> GitManAddonsConfig:
        result = self.to_dict(env_vars)
        filter = result[self.GITMAN_GROUP] or ""

        def flat_map(f: Callable[[str], List[str]], xs: List[str]) -> List[str]:
            ys = []
            for x in xs:
                ys.extend(f(x))
            return ys

        filters = filter.split()
        if filters:
            filters = flat_map(lambda it: it.split(","), filters)

        return GitManAddonsConfig(
            path=self.get_path(env_vars, result),
            name_filter=filters,
            no_locked_sources=result.get(self.GITMAN_NO_LOCKED_SOURCES).lower() == str(True).lower(),
            enable=not result.get(self.GITMAN_DISABLE).lower() == str(True).lower(),
        )


class OdooAddonsDef(abc.ABC):
    def __init__(self, name: str, gitman_config: GitManAddonsConfig = None):
        self.name = name
        self.gitman_config: GitManAddonsConfig = gitman_config or GitManAddonsConfig(self.addons_path)

    @property
    @abc.abstractmethod
    def addons_path(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def install_cmd(self) -> List[List[str]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def arg_cmd(self) -> List[str]:
        raise NotImplementedError()


PT = TypeVar("PT", bound="AddonsSuffix")


class ABCSubDirAddons(AddonsSuffix, abc.ABC):
    parent_addons: PT

    _parent_type: Type[PT] = None

    def __init__(self, base_key: str, prefix: str):
        assert self._parent_type, "Set _parent_type in %s" % type(self)
        super(ABCSubDirAddons, self).__init__(base_key, prefix)
        of_ref = base_key.split("_OF_")[-1]
        self.parent_addons = None
        if of_ref and self.is_valid():
            tmp = self._parent_type("")
            key_git = tmp.prefix + "_" + of_ref
            self.parent_addons = self._parent_type(key_git)
            assert self.parent_addons.is_valid(), "The key %s is not a Addons valid key" % key_git

    def is_valid(self) -> bool:
        return super().is_valid() and "_OF_" in self.base_key

    @property
    def identifier(self) -> str:
        return super().identifier

    def extract(self, env_vars: Dict[str, str]) -> BaseAddonsResult:
        res = self.to_dict(env_vars)
        return BaseAddonsResult(
            self.parent_addons.get_gitman_config(env_vars),
            name=self.NAME.full_key,
            full_path=self.get_path(env_vars, res),
        )

    def get_path(self, env_vars: Dict[str, str], res: Dict[KeySuffix, str]) -> str:
        parent_extract = self.parent_addons.extract(env_vars)
        sub_path = res[self.NAME]
        if os.path.isabs(sub_path):
            sub_path = sub_path[1:]  # Remove '/' at first, removeprefix don't exist in 3.8
        return os.path.join(parent_extract.addons_path, sub_path)


class AddonsInstallCmd(tuple):
    def __new__(cls: AddonsInstallCmd, cmd: List[str], args: List[str] = None) -> "AddonsInstallCmd":
        return super().__new__(cls, cmd + (args or []))

    def __init__(self, cmd: List[str], args: List[str] = None):
        super(AddonsInstallCmd, self).__init__(cmd + (args or []))
        self.cmd: List[str] = cmd
        self.args: List[str] = args or []


class BaseAddonsResult(OdooAddonsDef):
    def __init__(self, gitman: GitManAddonsConfig, name: str, full_path: str):
        super().__init__(name, gitman)
        self.name = name
        self._full_path = full_path

    def __str__(self):
        return f"{type(self).__name__}({self.name}, {self.addons_path})"

    __repr__ = __str__

    def install_cmd(self) -> List[List[str]]:
        if not self.gitman_config.enable:
            return []
        if not os.path.exists(self.addons_path) or not gitman.models.config.load_config(self.addons_path):
            return []
        result = [["gitman", "install", *self.arg_cmd()]]
        if self.gitman_config.no_locked_sources:
            result.append(["gitman", "update", "--skip-lock", *self.arg_cmd()])
        return result

    def arg_cmd(self) -> List[str]:
        if not self.gitman_config.enable:
            return []
        return self.gitman_config.name_filter

    @property
    def addons_path(self) -> str:
        return self._full_path
