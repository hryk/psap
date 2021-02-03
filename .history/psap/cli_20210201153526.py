"""Console script for psap."""
import argparse
import sys


def main():
    """Console script for psap."""
    parser = argparse.ArgumentParser()
     )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="0.1.0",
    )
    args = parser.parse_args()
    print(args.version)
    
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
