"""
Module to run the qbraid command line interface.

"""

import os
import subprocess
import sys

from ._version import __version__

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)


def main():
    """The subprocess.run function is used to run the script and pass arguments."""

    if sys.argv[1:] == ["--version"] or sys.argv[1:] == ["-V"]:
        print(f"qbraid-cli/{__version__}")
    else:
        result = subprocess.run(
            [os.path.join(BASE_DIR, "bin", "qbraid.sh")] + sys.argv[1:],
            text=True,
            capture_output=True,
            check=False,
        )

        if result.stdout:
            if len(sys.argv) == 4 and sys.argv[2] == "activate":
                line_lst = result.stdout.split("\n")
                line_lst = line_lst[:-1]  # remove trailing blank line
                bin_path = line_lst.pop()  # last line contains bin_path
                std_out = "\n".join(line_lst)  # all other lines are regular stdout
                print(std_out)
                # activate python environment using bin_path
                os.system(
                    f"cat ~/.bashrc {bin_path}/activate > {bin_path}/activate2 && "
                    rf"sed -i 's/echo -e/\# echo -e/' {bin_path}/activate2 && "
                    f"/bin/bash --rcfile {bin_path}/activate2"
                )
            else:
                print(result.stdout)
        if result.stderr:
            print(result.stderr)


if __name__ == "__main__":
    main()
