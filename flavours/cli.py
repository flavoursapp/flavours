import sys
import os

import flavours

flavours_path = os.path.abspath(os.path.dirname(flavours.__file__))


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    os.system(f"source {os.path.join(flavours_path, 'ide.sh')}")

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do. Return values are exit codes.

    return 0


if __name__ == "__main__":
    sys.exit(main())
