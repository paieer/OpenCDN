import sys
from argparse import ArgumentParser

parser = ArgumentParser(description="OpenCDN")
parser.add_argument(
    "--reset-configuration", action="store_true", help="Resets the configuration file"
)
parser.add_argument("--configuration-file", type=str, default="opencdn.conf")
parser.add_argument("-v", "--verbose", action="store_true", help="stdout info logs")
parser.add_argument("--clear-all-logs", action="store_true", help="Delete all files in the log directory")
parser.add_argument("--clear-today-log", action="store_true", help="Clear the today log file")

args = parser.parse_args(sys.argv[1:])
