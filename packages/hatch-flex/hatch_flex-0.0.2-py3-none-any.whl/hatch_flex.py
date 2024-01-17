""" Hatch Flex Plugin """

from hatchling.plugin import hookimpl
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


@hookimpl
def hatch_register_build_hook():
    return FlexBuildHook


class FlexBuildHook(BuildHookInterface):
    """
    Flex Plugin Hook

    Configuration:
        [build-system]
        requires = ["hatchling", "hatch-flex"]
        build-backend = "hatchling.build"

        [tool.hatch.build.hooks.flex]
        editable-dependencies = [...]
        standard-dependencies = [...]

    """

    PLUGIN_NAME = "flex"

    def initialize(self, version, build_data):
        key_name = f"{version}-dependencies"
        full_key = f"tool.hatch.build.hooks.{self.PLUGIN_NAME}.{key_name}"

        flex_deps = self.config.get(key_name, [])

        if not isinstance(flex_deps, list):
            raise TypeError(f"{full_key} must be an array")

        if not all(isinstance(s, str) for s in flex_deps):
            raise TypeError(f"Dependencies in {full_key} must be strings")

        if flex_deps:
            dependencies = build_data.get("dependencies", [])
            message = f"Adding {key_name} {flex_deps!r}"
            self.app.display_info(message)
            dependencies.extend(flex_deps)
