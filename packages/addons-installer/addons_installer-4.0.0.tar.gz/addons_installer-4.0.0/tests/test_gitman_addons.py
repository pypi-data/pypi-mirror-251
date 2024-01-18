import os
import unittest
from pathlib import Path
from typing import Any, Type, TypeVar, cast

from src.addons_installer.addons_installer import AddonsFinder
from src.addons_installer.api import BaseAddonsResult
from src.addons_installer.gitman_addons import GitManAddons

T = TypeVar("T")


class TestGitManAddons(unittest.TestCase):
    def setUp(self) -> None:
        self.test_repo_path = str(Path(__file__).parent.joinpath("repo").absolute())

    def assertType(self, inst: Any, type_to_assert: Type[T], msg: str = None) -> T:
        self.assertIsInstance(obj=inst, cls=type_to_assert, msg=msg)
        return cast(type_to_assert, inst)

    def test_discover_no_params(self):
        params = {"ADDONS_LOCAL_SRC_SAMPLE_REPO": str(self.test_repo_path)}

        addons = AddonsFinder.parse_env(params)

        print(addons)
        self.assertEqual(len(addons), 3, "Addons local src and the 2 inside gitman.yml with default group")
        self.assertEqual(
            ["ADDONS_LOCAL_SRC_SAMPLE_REPO", "common", "community"],
            [it.name for it in addons],
            """Les addons doivent être dans cette ordre et avec ces nom.
          L'ordre doit être celui de déclaration dans gitman.yml""",
        )
        local = self.assertType(addons[0], BaseAddonsResult)
        common = self.assertType(addons[1], GitManAddons)
        community = self.assertType(addons[2], GitManAddons)

        self.assertEqual(local.install_cmd(), [["gitman", "install"]])
        self.assertFalse(local.arg_cmd())

        self.assert_gitman_addons(local, community, "community")
        self.assert_gitman_addons(local, common, "common")

    def assert_gitman_addons(self, local: BaseAddonsResult, addon: GitManAddons, name_to_assert: str):
        self.assertEqual(
            addon.addons_path,
            os.path.join(local.addons_path, "dependency-modules", name_to_assert),
            "Correspond au chemin complet du projet local et de l'emplacement gitman",
        )
        self.assertFalse(addon.install_cmd(), "A gitman module is not installable, the Local drive the install")
        self.assertFalse(addon.arg_cmd())

    def test_disable_gitman(self):
        addons = AddonsFinder.parse_env(
            {
                "ADDONS_LOCAL_SRC_SAMPLE_REPO": str(self.test_repo_path),
                "ADDONS_LOCAL_SRC_SAMPLE_REPO_GITMAN_DISABLE": str(True),
            }
        )
        print(addons)
        self.assertEqual(len(addons), 1, "Only addons local src")
        self.assertEqual(["ADDONS_LOCAL_SRC_SAMPLE_REPO"], [it.name for it in addons])
        local = self.assertType(addons[0], BaseAddonsResult)
        self.assertFalse(local.install_cmd(), "No command to run for gitman")
        self.assertFalse(local.arg_cmd())

    def test_gitman_group_PROD(self):
        addons = AddonsFinder.parse_env(
            {
                "ADDONS_LOCAL_SRC_SAMPLE_REPO": str(self.test_repo_path),
                "ADDONS_LOCAL_SRC_SAMPLE_REPO_GITMAN_GROUP": "prod",
            }
        )
        print(addons)
        self.assertEqual(len(addons), 4, "Only addons local src and the group 'prod' members")
        self.assertEqual(
            ["ADDONS_LOCAL_SRC_SAMPLE_REPO", "common", "community", "s3_filestore"], [it.name for it in addons]
        )

        local = self.assertType(addons[0], BaseAddonsResult)
        common = self.assertType(addons[1], GitManAddons)
        community = self.assertType(addons[2], GitManAddons)
        s3_filestore = self.assertType(addons[3], GitManAddons)

        self.assertEqual(local.install_cmd(), [["gitman", "install", "prod"]])

        self.assert_gitman_addons(local, common, "common")
        self.assert_gitman_addons(local, community, "community")
        self.assert_gitman_addons(local, s3_filestore, "s3_filestore")

    def test_gitman_mulit_group(self):
        for group_case in ["code,prod", "code prod"]:
            with self.subTest("Test split group works", group_case=group_case):
                addons = AddonsFinder.parse_env(
                    {
                        "ADDONS_LOCAL_SRC_SAMPLE_REPO": str(self.test_repo_path),
                        "ADDONS_LOCAL_SRC_SAMPLE_REPO_GITMAN_GROUP": group_case,
                    }
                )
                self.assertEqual(len(addons), 4, "Only addons local src and the group 'prod' members")
                self.assertEqual(
                    ["ADDONS_LOCAL_SRC_SAMPLE_REPO", "common", "community", "s3_filestore"], [it.name for it in addons]
                )

                local = self.assertType(addons[0], BaseAddonsResult)
                common = self.assertType(addons[1], GitManAddons)
                community = self.assertType(addons[2], GitManAddons)
                s3_filestore = self.assertType(addons[3], GitManAddons)

                self.assertEqual([["gitman", "install", "code", "prod"]], local.install_cmd(), "Install request group")

                self.assert_gitman_addons(local, common, "common")
                self.assert_gitman_addons(local, community, "community")
                self.assert_gitman_addons(local, s3_filestore, "s3_filestore")

    def test_gitman_group_PROD_no_locked(self):
        addons = AddonsFinder.parse_env(
            {
                "ADDONS_LOCAL_SRC_SAMPLE_REPO": str(self.test_repo_path),
                "ADDONS_LOCAL_SRC_SAMPLE_REPO_GITMAN_GROUP": "prod",
                "ADDONS_LOCAL_SRC_SAMPLE_REPO_GITMAN_NO_LOCKED_SOURCES": str(True),
            }
        )
        print(addons)
        self.assertEqual(len(addons), 4, "Only addons local src and the group 'prod' members")
        self.assertEqual(
            ["ADDONS_LOCAL_SRC_SAMPLE_REPO", "common", "community", "s3_filestore"], [it.name for it in addons]
        )

        local = self.assertType(addons[0], BaseAddonsResult)
        common = self.assertType(addons[1], GitManAddons)
        community = self.assertType(addons[2], GitManAddons)
        s3_filestore = self.assertType(addons[3], GitManAddons)

        self.assertEqual(
            local.install_cmd(),
            [["gitman", "install", "prod"], ["gitman", "update", "--skip-lock", "prod"]],
            "Install request group without the locked source",
        )

        self.assert_gitman_addons(local, common, "common")
        self.assert_gitman_addons(local, community, "community")
        self.assert_gitman_addons(local, s3_filestore, "s3_filestore")
