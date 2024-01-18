import pytest
import subprocess
import pyimportcyclefinder


class TestCommandLineInterface:
    def test_cli_help_executes(self):
        status_code, output = subprocess.getstatusoutput(" ".join([
            "python", "-m", "pyimportcyclefinder.cli", "--help"
        ]))
        assert (status_code == 0)

    def test_cli_version_executes(self):
        command_args = [
            "python", "-m", "pyimportcyclefinder.cli", "--version"
        ]
        reply_prefix = " ".join(command_args[0: (len(command_args) -1)])
        status_code, output = subprocess.getstatusoutput(" ".join(command_args))
        reply_value = pyimportcyclefinder.__version__
        total_reply_message = f"{reply_prefix}, version {reply_value}"
        print(total_reply_message)
        print(output)
        assert (status_code == 0 and output == total_reply_message)
