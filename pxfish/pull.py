"""
Functions for pulling Operation Type and Library files from Aquarium.
"""

import json
import logging
import os
from operation_types import (
    operation_type_code_names
)
from paths import (
    create_named_path,
    create_operation_path,
    create_library_path,
    makedirectory
)


def field_type_list(field_types, role):
    """
    Returns the sublist of field types with the given role.

    Arguments:
      field_types (list): the list of field types
      role (string): the role of field types to be returned

    Returns:
      list: the sublist of field_types that have the role
    """
    ft_list = []
    for field_type in field_types:
        if field_type.role == role:
            ft_ser = {
                "name": field_type.name,
                "part": field_type.part,
                "array": field_type.array,
                "routing": field_type.routing
            }
            ft_list.append(ft_ser)
    return ft_list


def get_library(aq, path, category, library):
    """
    Retrieves a single Library Object

    Arguments:
        aq (Session Object): Aquarium session object
        path (String): the path to where the file will be written
        category (String): The category the Library is in
        library (String): The Library to be retrieved
    """
    library = aq.Library.where({"category": category, "name": library})
    if not library:
        pull(path, operation_types=[], libraries=library)


def get_operation_type(aq, path, category, operation_type):
    """
    Retrieves a single Operation Type Object

    Arguments:
        aq (Session Object): Aquarium session object
        path (String): the path to where the file will be written
        category (String): The category the OperationType is in
        operation_type (String): The OperationType to be retrieved
    """
    operation_type = aq.OperationType.where(
        {"category": category, "name": operation_type})
    pull(path, operation_types=operation_type)


def get_category(aq, path, category):
    """
    Retrieves all the Libraries and Operation Types within a category

    Arguments:
        aq (Session Object): Aquarium session object
        path (String): the path to where the files will be written
        category (String): the category name
    """
    operation_types = aq.OperationType.where({"category": category})
    libraries = aq.Library.where({"category": category})
    pull(path, operation_types=operation_types, libraries=libraries)


def get_all(aq, path):
    """
    Retrieves all Operation Types and Libraries

    Arguments:
        aq (Session Object): Aquarium session object
        path (String): the path to where the files will be written
    """
    operation_types = aq.OperationType.all()
    libraries = aq.Library.all()
    pull(path, operation_types, libraries)


def pull(path, operation_types=[], libraries=[]):
    """
    Pulls OperationType and/or Library files from the Aquarium instance.

    Arguments:
        path (String): the path for the directory where files should be written
        operation_types (List): list of OperationTypes whose files to pull
        libraries (List): list of Libraries whose files to pull
    """
    for operation_type in operation_types:
        write_operation_type(path, operation_type)

    for library in libraries:
        write_library(path, library)


def write_code(path, file_name, code_object):
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


def write_definition_json(file_path, operation_type):
    """
    Writes the definition of the operation_type as JSON to the given file path.

    Arguments:
      file_path (string): the path of the file to write
      operation_type (OperationType): the operation type for definition
    """
    ot_ser = {}
    ot_ser["id"] = operation_type.id
    ot_ser["name"] = operation_type.name
    ot_ser["parent_class"] = "OperationType"
    ot_ser["category"] = operation_type.category
    ot_ser["inputs"] = field_type_list(operation_type.field_types, 'input')
    ot_ser["outputs"] = field_type_list(operation_type.field_types, 'output')
    ot_ser["on_the_fly"] = operation_type.on_the_fly
    ot_ser["user_id"] = operation_type.protocol.user_id

    with open(file_path, 'w') as file:
        file.write(json.dumps(ot_ser, indent=2))


def write_library_definition_json(file_path, library):
    """
    Writes the definition of library as JSON to the given file path.

    Arguments:
      file_path (string): the path to the file as written
      library (Library): the library for which the definition should be written
    """
    library_ser = {}
    library_ser["id"] = library.id
    library_ser["name"] = library.name
    library_ser["parent_class"] = "Library"
    library_ser["category"] = library.category
    library_ser["user_id"] = library.source.user_id

    with open(file_path, 'w') as file:
        file.write(json.dumps(library_ser, indent=2))


def write_operation_type(path, operation_type):
    """
    Writes the files associated with the operation_type to the path.

    Arguments:
      path (string): the path to where the files will be written
      operation_type (OperationType): the operation type being written
    """
    logging.info("writing operation type {}".format(operation_type.name))

    category_path = create_named_path(path, operation_type.category)
    makedirectory(category_path)
    path = create_operation_path(category_path, operation_type.name)
    makedirectory(path)
    code_names = operation_type_code_names()

    for name in code_names:
        code_object = operation_type.code(name)
        if not code_object:
            logging.warning(
                "Missing {} code for operation type {}".format(
                    operation_type.name, name)
            )
            continue

        file_name = "{}.rb".format(name)
        try:
            write_code(path, file_name, code_object)
        except OSError as error:
            logging.warning(
                "Error {} writing file {} for operation type {}".format(
                    error, file_name, operation_type.name))
            continue
        except UnicodeError as error:
            logging.warning(
                "Encoding error {} writing file {} for operation type {}".format(
                    error, file_name, operation_type.name))
            continue

    write_definition_json(
        os.path.join(path, 'definition.json'),
        operation_type
    )


def write_library(path, library):
    """
    Writes the files for the library to the path.

    Arguments:
      path (string): the path of the file to write
      library (Library): the library whose definition will be written
    """
    logging.info("writing library {}".format(library.name))

    category_path = create_named_path(path, library.category)
    makedirectory(category_path)
    library_path = create_library_path(category_path, library.name)
    makedirectory(library_path)

    code_object = library.code("source")
    if not code_object:
        logging.warning(
            "Ignored library {} missing library code".format(
                library.name)
        )
    file_name = 'source.rb'
    try:
        write_code(library_path, file_name, code_object)
    except OSError as error:
        logging.warning("Error {} writing file {} for library {}".format(
            error, file_name, library.name))
    except UnicodeError as error:
        logging.warning(
            "Encoding error {} writing file {} for library {}".format(
                error, file_name, library.name))

    write_library_definition_json(os.path.join(
        library_path, 'definition.json'), library)