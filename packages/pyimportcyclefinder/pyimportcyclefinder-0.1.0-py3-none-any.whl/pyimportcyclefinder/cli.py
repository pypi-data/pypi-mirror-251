import re
from pathlib import Path
from pyimportcyclefinder.find_cycles import find_cycles
import click
old_print = print
import pyimportcyclefinder
try:
    import rich
    import rich.pretty
    rich.pretty.install()
    print = rich.print
except ModuleNotFoundError as e:
    print = old_print


@click.command()
@click.argument(
    "package_root",
    type=click.Path(path_type=Path, file_okay=False, dir_okay=True, readable=True, writable=False),
)
@click.version_option(pyimportcyclefinder.__version__)
def main(package_root: Path):
    cycles = find_cycles(package_root)
    newline = "\n"
    print("All cycles without nested imports included:\n", f"->{newline}".join(cycles[0]))
    print("\nCycles with a path back to themselves using the above graph (not including other nested imports):")
    for package, path in cycles[1].items():
        print(f'{package}{f"->{newline}".join(path)}')
    print("\nAll cycles if function nested imports are included:", f'{newline}{f"->{newline}".join(cycles[2])}')

    # print(cycles[3].nodes, f"\n{cycles[3].edges}")


if __name__ == "__main__":
    main()
