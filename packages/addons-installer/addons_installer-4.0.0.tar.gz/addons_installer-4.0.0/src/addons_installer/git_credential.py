from __future__ import annotations

import dataclasses
import logging
from typing import Dict, List
from urllib.parse import urlparse

from .api import EnvKeyExtractor, ExtractorManager

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

PROTOCOLE_HTTPS = "https"
PROTOCOLE_SSH = "ssh"
PROTOCOLE_PUBLIC = "public"
FORMAT_GIT_CLONE = {
    PROTOCOLE_HTTPS: "https://%(login)s:%(password)s@%(server)s/%(git_path)s",
    PROTOCOLE_SSH: "git@%(server)s:%(git_path)s",
    PROTOCOLE_PUBLIC: "https://%(server)s/%(git_path)s",
}


@dataclasses.dataclass
class GitCredential:
    name: str
    host: str
    username: str
    password: str
    path: str = ""

    def git_uri(self, format: str = "https") -> str:
        return FORMAT_GIT_CLONE[format] % {
            "login": self.username,
            "password": self.password,
            "server": self.host,
            "git_path": self.path,
        }


class AddonsCredentialGit(EnvKeyExtractor[GitCredential]):
    """
    Represent a Git remote url to clone to get Odoo Addons.

    """

    def __init__(self, base_key):
        super(AddonsCredentialGit, self).__init__(base_key, "CREDENTIAL_GIT")
        self.LOGIN = self.create_key("HTTPS_LOGIN", have_default=False)
        self.PASSWORD = self.create_key("HTTPS_PASSWORD", have_default=False)

    def extract(self, env_vars: Dict[str, str]) -> GitCredential:
        res = self.to_dict(env_vars)
        name = res[self.NAME]
        if not name.startswith("http"):
            name = "https://" + name
        parsed = urlparse(name)
        parsed = parsed._replace(path=parsed.path[1:])
        return GitCredential(
            name=self.base_key,
            host=parsed.hostname,
            username=res[self.LOGIN],
            password=res[self.PASSWORD],
            path=parsed.path,
        )


class GitCredentialManager(ExtractorManager[AddonsCredentialGit]):
    def __init__(self, env_vars: Dict[str, str] = None):
        super(GitCredentialManager, self).__init__(AddonsCredentialGit, env_vars=env_vars)

    def get_cmd(self, git_credential: GitCredential) -> List[str]:
        cmd_config_global = ["git", "config", "--global"]
        cmd_config_global.append(f"""url."{git_credential.git_uri("https")}".insteadOf""")
        cmd_config_global.append(f'"{git_credential.git_uri("ssh")}"')
        return cmd_config_global
