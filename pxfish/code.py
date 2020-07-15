"""
Functions for writing code to files, or creating code objects
"""
import logging
import os


def write(path, file_name, code_object):
    """
    Writes the aquarium code object to the given path.

    Arguments:
      path (string): the path of the file to be written
      file_name (string): the name of the file to be written
      code_object (Code): the code object
    """
    file_path = os.path.join(path, file_name)
    with open(file_path, 'w') as file:
        file.write(code_object.content)


def create_code_objects(aq, component_names):
    """
    Creates code objects for each named component.

    Arguments:
        aq (Session Object): Aquarium session object
        component_names (List): names of code components
    """
    code_objects = {}
    for name in component_names:
        code_objects[name] = aq.Code.new(name=name, content='')
    return code_objects


def read(*, path, name):
    file_name = "{}.rb".format(name)
    try:
        with open(os.path.join(path, file_name)) as f:
            return f.read()
    except FileNotFoundError as error:
        logging.warning(
            "Error {} reading expected code file {}".format(
                error, file_name))
        return None