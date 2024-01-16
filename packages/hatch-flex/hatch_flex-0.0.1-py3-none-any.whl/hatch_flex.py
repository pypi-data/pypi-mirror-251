from pprint import pprint

from hatchling.plugin import hookimpl
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


@hookimpl
def hatch_register_build_hook():
    return FlexBuildHook


def dump_vars(**kwargs):
    for k, v in kwargs.items():
        print(k)
        pprint(v)


def dump_obj(obj, attribs=None):
    if isinstance(attribs, str):
        attribs = attribs.split()
    elif attribs is None:
        attribs = dir(obj)

    for attrib in attribs:
        value = getattr(obj, attrib, None)
        print(attrib)
        pprint(value)


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
        dependencies = build_data.get("dependencies", [])
        flex_deps = self.config.get(f"{version}-dependencies", [])

        if flex_deps:
            message = f"Adding flex dependencies {flex_deps!r}"
            self.app.display_info(message)
            dependencies.extend(flex_deps)
