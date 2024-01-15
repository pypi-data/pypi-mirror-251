from typing import Union

from argrelay.enum_desc.PluginType import PluginType
from argrelay.runtime_context.AbstractPlugin import AbstractPlugin


class AbstractConfigurator(AbstractPlugin):
    """
    `PluginType.ConfiguratorPlugin` implements logic to configure `argrelay` server
    when static config is not good enough.
    """

    def get_plugin_type(
        self,
    ) -> PluginType:
        return PluginType.ConfiguratorPlugin

    def provide_project_git_commit_display_string(
        self,
    ) -> Union[str, None]:
        """
        Returns commit id (in any format) to be shown as is.

        This commit display string is used as text for a link (purely display function).

        The link itself is generated by concatenating two components - see:
        *   `provide_project_commit_id_url_prefix`
        *   `provide_project_git_commit_id`
        """
        return None

    def provide_project_commit_id_url_prefix(
        self,
    ) -> Union[str, None]:
        """
        Returns a URL prefix to be concatenated with `provide_project_git_commit_id` to form a URL.

        The display text for the link is taken from `provide_project_git_commit_display_string` instead.
        """
        return None

    def provide_project_git_commit_id(
        self,
    ) -> Union[str, None]:
        """
        Returns commit id in specific format (e.g. full) which should work as part of a URL.

        It is concatenated with `provide_project_git_commit_id_url_prefix` to form a URL.

        The display text for the link is taken from `provide_project_git_commit_display_string` instead.
        """
        return None

    def provide_project_git_commit_time(
        self,
    ) -> Union[int, None]:
        """
        Return commit time in seconds since epoch (Unix time).

        The commit time should normally be taken for the same commit id as `provide_project_git_commit_id`.
        """
        return None
