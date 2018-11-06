""" Methods to interact with blocks for the purpsoses of defining the spec """

from importlib import import_module
import sys
from os import getcwd
from os.path import basename, dirname, isfile, join


def build_spec_for_block(block_path):
    block = _get_block_class(block_path)
    block_spec = {}
    properties = block.get_description()["properties"]
    block_version = properties["version"]["default"]
    try:
        major, minor, build = block_version.split(".")
    except ValueError:
        raise ValueError("{} is an invalid version".format(block_version))
    # We only use the major and minor version of a block for the spec
    block_spec["version"] = "{}.{}.0".format(major, minor)
    block_spec["properties"] = _build_properties_spec(block)
    block_spec["commands"] = _build_commands_spec(block)
    block_spec["inputs"] = _build_inputs_spec(block)
    block_spec["outputs"] = _build_outputs_spec(block)
    return block_spec


def build_release_for_block(block_path):
    block = _get_block_class(block_path)
    block_release = {}
    properties = block.get_description()["properties"]
    block_release["version"] = properties["version"]["default"]
    return block_release


def _build_properties_spec(block):
    properties_spec = {}
    properties = block.get_description()["properties"]
    for k, property in properties.items():
        if k in ["id", "type", "name", "version", "log_level"]:
            continue
        property_spec = {}
        property_spec["title"] = property["title"]
        property_spec["type"] = property["type"]
        if "default" in property:
            property_spec["default"] = property["default"]
        properties_spec[k] = property_spec
    return properties_spec


def _build_commands_spec(block):
    commands_spec = {}
    commands = block.get_description()["commands"]
    for k, command in commands.items():
        if k in ['properties']:
            continue
        command_spec = {}
        command_spec["params"] = command["params"]
        commands_spec[command["title"]] = command_spec
    return commands_spec


def _build_inputs_spec(block):
    inputs_spec = {}
    inputs = block.inputs()
    for input_object in inputs:
        input_label = input_object.get_description()["label"]
        inputs_spec[input_label] = {"description": ""}
    return inputs_spec


def _build_outputs_spec(block):
    outputs_spec = {}
    outputs = block.outputs()
    for output_object in outputs:
        output_label = output_object.get_description()["label"]
        outputs_spec[output_label] = {"description": ""}
    return outputs_spec


def _get_block_class(block_path):
    try:
        block_module_path, block_class_name = block_path.rsplit('.', 1)
    except ValueError:
        print("ERROR: Invalid from_python value. Make sure to specify the "
              "value as 'path.to.block_file.BlockClass'")
        raise
    block_module = import_module("{}.{}".format(
        _find_current_namespace(), block_module_path))
    block_class = getattr(block_module, block_class_name)
    return block_class


def _find_current_namespace():
    """ Walk up the tree looking for __init__.py to figure out where we are.

    This method will start in the working directory and keep walking up a
    directory until we get to one that doesn't have an __init__.py in it. This
    allows the method to be run from anywhere within the namespace and figure
    out where the root of the namespace is.

    It will also add the root of the namespace to the Python path if it isn't
    there already so that things can be imported from it.

    Returns:
        namespace (str): Dot-separated namespace string (e.g., 'path.to.me')
    """
    namespace_parts = []
    starting_dir = getcwd()
    while isfile(join(starting_dir, '__init__.py')):
        namespace_parts.insert(0, basename(starting_dir))
        starting_dir = dirname(starting_dir)
    if starting_dir not in sys.path:
        sys.path.append(starting_dir)
    return ".".join(namespace_parts)
