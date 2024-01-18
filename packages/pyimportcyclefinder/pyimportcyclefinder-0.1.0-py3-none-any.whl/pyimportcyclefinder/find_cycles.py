import ast
import copy
import rich
import rich.pretty
import functools
import re
from ast import AST, Import, ImportFrom, FunctionDef, AsyncFunctionDef, parse
from collections import deque
from pathlib import Path
from typing import Deque, List, Dict, Union, Set, Iterable, Optional, AnyStr, Tuple
import networkx as nx
import regex
from pyimportcyclefinder.protocol.re import PatternProtocol
from pyimportcyclefinder.protocol.regex import ExtendedPatternProtocol
from pyimportcyclefinder.validator import configured_validate_call


@configured_validate_call
def get_imports_for_code_file_using_ast(python_file: Path) -> Dict[str, Set[str]]:
    import_package_pattern = regex.compile(r"^import (?P<std_imp_module>\S+?)(?: as .+)?$", flags=regex.V1)
    from_package_import_pattern = regex.compile(
        r"^from (?P<from_imp_module>\S.+?) import (?:(?:[(][^()]+[)])|(?:[^()]+))$",
        flags=regex.V1
    )
    AnImport = Union[Import, ImportFrom]
    AnyFuncDef = Union[FunctionDef, AsyncFunctionDef]
    imported_package_names = {"nested": set(), "module_level": set()}
    with python_file.open("rt") as fh:
        lines = fh.readlines()
        document = "".join(lines)
        ast_ = parse(document)
        queue = deque()  # type: Deque[Tuple[AST,int,bool]]
        queue.append((ast_, 0, False))
        # print(ast.dump(ast_))
        while len(queue) > 0:
            element, depth, inside_a_def = queue.popleft()
            # print("Element Type: ", type(element), depth, "inside a def", inside_a_def)
            if isinstance(element, AnImport):
                import_statement = ast.unparse(element)
                if isinstance(element, Import):
                    m = import_package_pattern.match(import_statement)
                    if not m:
                        raise ValueError("Failed to parse ImportPackage statement:", import_statement)
                    source_package = m.capturesdict()['std_imp_module'][0]
                elif isinstance(element, ImportFrom):
                    m = from_package_import_pattern.match(import_statement)
                    if not m:
                        raise ValueError("Failed to parse FromPackageImport statement:", import_statement)
                    source_package = m.capturesdict()['from_imp_module'][0]
                else:
                    raise ValueError(
                        "Got an AST Node that looked like an Import previously but wasn't an import when checked"
                    )
                if inside_a_def:
                    # print("\tImport is inside a definition (Class/Func etc")
                    imported_package_names['nested'].add(source_package)
                else:
                    # print("\tImport is not inside a definition")
                    imported_package_names['module_level'].add(source_package)
                continue
            for child in ast.iter_child_nodes(element):
                if isinstance(element, AnyFuncDef):
                    # print("\t", type(child), "is a def, appending tuple with True")
                    queue.append((child, depth + 1, True))
                else:
                    # print("\t", type(child), "is not a def, appending tuple with False")
                    queue.append((child, depth + 1, False))

        return imported_package_names


@configured_validate_call
def read_imports_from_python_files(
        m2f: Dict[str, Path],
        # single_line_import_patterns: List[CompiledPatternType] = (
        #     regex.compile(r"^import (?P<std_imp_module>\S+?)(?: as .+)$", flags=regex.V1),
        #     regex.compile(r"^from (?P<from_imp_module>\S.+?) import (?:(?:[(][^()]+[)])|(?:[^()]+))$", flags=regex.V1)
        # ),
        # multi_line_import_pattern_sets: Iterable[CompiledMultiLinePatternSetType] = (
        #         (
        #                 regex.compile(r"^from (?P<from_imp_module>\S.+?) import [(][^()]+$", flags=regex.V1),
        #                 regex.compile("^[^()]+$", flags=regex.V1),
        #                 regex.compile(r"^[^()]+[)].*$", flags=regex.V1),
        #         )
        # )
) -> Dict[str, Dict[str, Set[str]]]:
    """

    :param m2f:
    :return:
    """
    module_names_to_imports = dict()
    for module_name, file_path in m2f.items():
        module_names_to_imports[module_name] = get_imports_for_code_file_using_ast(file_path)
    return module_names_to_imports


@configured_validate_call
def find_python_modules_and_packages(
        package_root: Path
) -> Dict[str, Path]:
    """

    :param package_root:
    :return:
    """
    module_names_to_source_files = dict()
    source_paths = deque()
    source_paths.append(package_root)

    while len(source_paths):
        next_source_item = source_paths.popleft()
        for sub_item in next_source_item.glob("*"):
            if sub_item.name == "__pycache__":
                continue
            if sub_item.is_dir():
                source_paths.append(sub_item)
                continue
            if sub_item.is_file():
                if sub_item.name == "__init__.py":
                    module_name = '.'.join(list(sub_item.parent.parts))
                else:
                    module_name = '.'.join(list((sub_item.parent / sub_item.stem).parts))
                module_names_to_source_files[module_name] = sub_item
    return module_names_to_source_files


@configured_validate_call
def assemble_import_graph(module_names_to_imports: Dict[str, Dict[str, Set[str]]]) -> Tuple[nx.DiGraph, nx.DiGraph]:
    """

    :param module_names_to_imports:
    :return:
    """
    Graphs = {
        'G_without_nested': nx.DiGraph(),
        'G_with_nested': nx.DiGraph()
    }
    node_names = set()
    node_names.update(list(module_names_to_imports.keys()))
    for package_name, package_import_dict in module_names_to_imports.items():
        nested_import_set = package_import_dict['nested']
        module_level_import_set = package_import_dict['module_level']
        for dest_import in module_level_import_set:
            Graphs['G_with_nested'].add_node(package_name)
            Graphs['G_without_nested'].add_node(package_name)
            Graphs['G_with_nested'].add_node(dest_import)
            Graphs['G_without_nested'].add_node(dest_import)
            Graphs['G_with_nested'].add_edge(package_name, dest_import)
            Graphs['G_without_nested'].add_edge(package_name, dest_import)
        for dest_import in nested_import_set:
            Graphs['G_with_nested'].add_node(package_name)
            Graphs['G_without_nested'].add_node(package_name)
            Graphs['G_with_nested'].add_node(dest_import)
            Graphs['G_without_nested'].add_node(dest_import)
            Graphs['G_with_nested'].add_edge(package_name, dest_import)
    return Graphs['G_without_nested'], Graphs['G_with_nested']


@configured_validate_call
def find_cycles(
        package_root: Union[Path, str]
) -> Tuple[List[str], Dict[str, List[str]], List[str], nx.DiGraph, nx.DiGraph]:
    rich.pretty.install()
    if isinstance(package_root, str):
        base_path = Path(package_root)
    else:
        base_path = package_root
    m2f = find_python_modules_and_packages(base_path)

    module_names_to_imports = read_imports_from_python_files(m2f)

    # rich.pretty.pprint(module_names_to_imports)

    G, G_with_all_nested_edges = assemble_import_graph(module_names_to_imports)
    cycles_at_module_and_class_level = ["->".join(x) for x in list(nx.recursive_simple_cycles(G))]
    # rich.print(cycles_at_module_and_class_level)
    cycles_from_nested_imports_if_all_in_graph = ["->".join(x) for x in list(nx.recursive_simple_cycles(G_with_all_nested_edges))]
    # rich.print(cycles_from_nested_imports_if_all_in_graph)

    cycles_from_nested_imports = dict()
    for package, package_imports in module_names_to_imports.items():
        for nested_import in package_imports['nested']:
            path_from_import_to_self = list(nx.all_simple_paths(G, nested_import, package))
            # print(path_from_import_to_self)
            if not(path_from_import_to_self is None or len(path_from_import_to_self) == 0):
                cycles_from_nested_imports[package] = list(path_from_import_to_self)
    return (
        cycles_at_module_and_class_level,
        cycles_from_nested_imports,
        cycles_from_nested_imports_if_all_in_graph,
        G,
        G_with_all_nested_edges
    )


__all__ = [
    find_cycles
]
