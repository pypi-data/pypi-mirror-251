import unittest
from typing import TypeVar

from src.addons_installer.git_credential import (
    AddonsCredentialGit,
    GitCredentialManager,
)

T = TypeVar("T")


class TestGitCredentialInstall(unittest.TestCase):
    def test_1(self):
        manager = GitCredentialManager(
            {
                "CREDENTIAL_GIT_MY_PROJECT": "gitlab.my-company.fr",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_LOGIN": "gitlab_login",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_PASSWORD": "gitlab_password",
            }
        )
        extractors = manager.create_extractors()
        self.assertEqual(1, len(extractors))
        commands = manager.get_cmd(manager.extract(extractors[0])[0])
        self.assertEqual(
            [
                "git",
                "config",
                "--global",
                'url."https://gitlab_login:gitlab_password@gitlab.my-company.fr/".insteadOf',
                '"git@gitlab.my-company.fr:"',
            ],
            commands,
        )

    def test_2(self):
        manager = GitCredentialManager(
            {
                "CREDENTIAL_GIT_MY_PROJECT": "gitlab.my-company.fr/group/project.git",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_LOGIN": "gitlab_login",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_PASSWORD": "gitlab_password",
            }
        )
        extractors = manager.create_extractors()
        self.assertEqual(1, len(extractors))
        commands = manager.get_cmd(manager.extract(extractors[0])[0])
        self.assertEqual(
            [
                "git",
                "config",
                "--global",
                'url."https://gitlab_login:gitlab_password@gitlab.my-company.fr/group/project.git".insteadOf',
                '"git@gitlab.my-company.fr:group/project.git"',
            ],
            commands,
        )


class TestGitCredentialEtract(unittest.TestCase):
    def setUp(self):
        self.ad_suffix = AddonsCredentialGit("MY_PROJECT")

    def test_no_path(self):
        res = self.ad_suffix.extract(
            {
                "CREDENTIAL_GIT_MY_PROJECT": "gitlab.my-company.fr",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_LOGIN": "gitlab_login",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_PASSWORD": "gitlab_password",
            }
        )

        self.assertEqual("gitlab_login", res.username)
        self.assertEqual("gitlab_password", res.password)
        self.assertEqual("", res.path)

        self.assertEqual("https://gitlab_login:gitlab_password@gitlab.my-company.fr/", res.git_uri("https"))
        self.assertEqual("git@gitlab.my-company.fr:", res.git_uri("ssh"))
        self.assertEqual("https://gitlab.my-company.fr/", res.git_uri("public"))

    def test_partial_path(self):
        res = self.ad_suffix.extract(
            {
                "CREDENTIAL_GIT_MY_PROJECT": "gitlab.my-company.fr/group",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_LOGIN": "gitlab_login",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_PASSWORD": "gitlab_password",
            }
        )

        self.assertEqual("gitlab_login", res.username)
        self.assertEqual("gitlab_password", res.password)
        self.assertEqual("group", res.path)

        self.assertEqual("https://gitlab_login:gitlab_password@gitlab.my-company.fr/group", res.git_uri("https"))
        self.assertEqual("git@gitlab.my-company.fr:group", res.git_uri("ssh"))
        self.assertEqual("https://gitlab.my-company.fr/group", res.git_uri("public"))

    def test_full_path(self):
        res = self.ad_suffix.extract(
            {
                "CREDENTIAL_GIT_MY_PROJECT": "gitlab.my-company.fr/group/sub/project.git",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_LOGIN": "gitlab_login",
                "CREDENTIAL_GIT_MY_PROJECT_HTTPS_PASSWORD": "gitlab_password",
            }
        )

        self.assertEqual("gitlab_login", res.username)
        self.assertEqual("gitlab_password", res.password)
        self.assertEqual("group/sub/project.git", res.path)
        self.assertEqual(
            "https://gitlab_login:gitlab_password@gitlab.my-company.fr/group/sub/project.git", res.git_uri("https")
        )
        self.assertEqual("git@gitlab.my-company.fr:group/sub/project.git", res.git_uri("ssh"))
        self.assertEqual("https://gitlab.my-company.fr/group/sub/project.git", res.git_uri("public"))
