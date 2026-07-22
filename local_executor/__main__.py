import sys

from .cli import _maintenance, main

maintenance_result = _maintenance(sys.argv[1:])
raise SystemExit(main() if maintenance_result is None else maintenance_result)
