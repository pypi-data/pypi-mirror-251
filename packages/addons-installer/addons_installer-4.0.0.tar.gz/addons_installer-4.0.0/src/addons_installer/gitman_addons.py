import logging
import os
from typing import List

import gitman
from gitman.models.source import Source

from .api import BaseAddonsResult, GitManAddonsConfig

_logger = logging.getLogger(__name__)


class GitManAddons(BaseAddonsResult):
    def __init__(self, gitman_config: GitManAddonsConfig, location_path: str, source: gitman.models.source.Source):
        super(GitManAddons, self).__init__(gitman_config, source.name, os.path.join(location_path, source.name))

    def install_cmd(self) -> List[List[str]]:
        return []

    def arg_cmd(self) -> List[str]:
        return []


def _get_sources_filter(self, names: List[str], sources: List[Source], skip_default_group: bool) -> List[str]:
    """Get a filtered subset of sources."""
    names_list = list(names)
    if not names_list and not skip_default_group:
        names_list.append(self.default_group)

    # Add sources from groups
    groups_filter = [group for group in self.groups if group.name in names_list]
    sources_filter = [member for group in groups_filter for member in group.members]

    # Add independent sources
    sources_filter.extend([source.name for source in sources if source.name in names_list])

    # Fall back to all sources if allowed
    if not sources_filter:
        if names and names_list != ["all"]:
            print(f"No dependencies match: {' '.join(names)}")
        else:
            sources_filter = [source.name for source in sources if source.name]

    return list(dict.fromkeys(sources_filter).keys())


def find_addons(config: GitManAddonsConfig) -> List[BaseAddonsResult]:
    gm_config = gitman.models.config.load_config(config.path)
    # TODO correctly use use_locked
    gm_sources = gm_config._get_sources(use_locked=None)
    sources_filters = _get_sources_filter(
        self=gm_config, names=config.name_filter, sources=gm_config.sources, skip_default_group=False
    )
    result: List[GitManAddons] = []
    src_by_name = {src.name: src for src in gm_sources}
    for source_filter in sources_filters:
        source = src_by_name.get(source_filter)
        if not source:
            _logger.info("Skipped dependency: %s", source_filter)
            continue
        result.append(GitManAddons(config, gm_config.location_path, source))
    return result
